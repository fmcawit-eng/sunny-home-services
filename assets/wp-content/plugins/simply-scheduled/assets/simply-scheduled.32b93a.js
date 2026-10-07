(function () {
    'use strict';

    var overlay = document.getElementById('scheduledOverlay');
    if (!overlay || typeof ScheduledCfg === 'undefined') return;

    var now = new Date();
    var TODAY = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var MAXD = new Date(TODAY); MAXD.setDate(MAXD.getDate() + (ScheduledCfg.horizonDays || 30));
    var WINDOWS = (ScheduledCfg.windows && ScheduledCfg.windows.length) ? ScheduledCfg.windows : ['8 AM \u2013 12 PM', '12 PM \u2013 6 PM'];

    // ── UTM / tracking capture ──────────────────────────────────────────
    // Captures on first landing and persists across the session (sessionStorage),
    // so the value survives even if the booking widget is opened on a later pageview
    // within the same visit, after the original query string is gone.
    var UTM_KEYS = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content','gclid','fbclid'];
    function _captureUtm() {
        // Always start from whatever is already stored (earlier page in same session)
        var stored = {};
        try { stored = JSON.parse(sessionStorage.getItem('sch_utm') || '{}'); } catch(e) {}
        // Merge current page URL params on top — URL params win so a fresh click always overrides
        var params = new URLSearchParams(window.location.search);
        var found = false;
        UTM_KEYS.forEach(function(k){
            var v = params.get(k);
            if (v) { stored[k] = v; found = true; }
        });
        // Persist back whenever anything changed
        if (found) {
            try { sessionStorage.setItem('sch_utm', JSON.stringify(stored)); } catch(e) {}
        }
        return stored;
    }
    // Re-read at submit time so multi-page visits always carry the latest stored values
    function _getUtm() {
        try { return JSON.parse(sessionStorage.getItem('sch_utm') || '{}'); } catch(e) { return {}; }
    }
    var UTM_PARAMS = _captureUtm();

    // ── Shared click-to-call helper ─────────────────────────────────────
    function _phoneLinkHtml() {
        var phoneDisplay = ScheduledCfg.phoneDisplay || '(763) 515-7881';
        var phoneRaw = ScheduledCfg.phoneRaw || phoneDisplay.replace(/\D/g,'');
        return '<a href="tel:'+esc(phoneRaw)+'" rel="noopener noreferrer" target="_parent" class="sch-phone-link">'+esc(phoneDisplay)+'</a>';
    }

    // ── Session UUID ─────────────────────────────────────────────────────
    // Persisted in sessionStorage so it survives page-to-page navigation within
    // the same browser session (tab). A new UUID is only created on a fresh session.
    function _makeUUID() {
        // UUID v4 — uses crypto.getRandomValues when available, falls back to Math.random
        if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
            var buf = new Uint8Array(16);
            crypto.getRandomValues(buf);
            buf[6] = (buf[6] & 0x0f) | 0x40; // version 4
            buf[8] = (buf[8] & 0x3f) | 0x80; // variant
            var hex = Array.from(buf).map(function(b){ return ('0'+b.toString(16)).slice(-2); });
            return [hex.slice(0,4),hex.slice(4,6),hex.slice(6,8),hex.slice(8,10),hex.slice(10)].map(function(g){return g.join('');}).join('-');
        }
        // Fallback
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random()*16|0, v = c==='x' ? r : (r&0x3|0x8);
            return v.toString(16);
        });
    }
    function _getSessionId() {
        var key = 'sch_session_id';
        try {
            var existing = sessionStorage.getItem(key);
            if (existing) return existing;
            var id = _makeUUID();
            sessionStorage.setItem(key, id);
            return id;
        } catch(e) {
            // sessionStorage blocked (private browsing with strict settings) — ephemeral fallback
            return _makeUUID();
        }
    }
    var _sid    = _getSessionId();
    var _stepTs = Date.now();

    function _log(step, extra) {
        var p = { step: step, session_id: _sid };
        try { p.page_url = window.location.pathname; } catch(e) {}
        if (extra) Object.keys(extra).forEach(function(k) { p[k] = String(extra[k] == null ? '' : extra[k]).slice(0, 200); });
        var body = new URLSearchParams();
        body.append('action', 'simply_scheduled_log');
        Object.keys(p).forEach(function(k) { body.append(k, p[k]); });
        fetch(ScheduledCfg.ajaxUrl, { method: 'POST', body: body }).catch(function() {});
    }
    function _logStep(step, extra) {
        var ms = Date.now() - _stepTs; _stepTs = Date.now();
        var d = extra || {}; d.duration_ms = ms;
        _log(step, d);
    }

    // Zip validation helpers
    function _zipIcon(html) { var ic=$('schZipIcon'); if(ic) ic.innerHTML=html; }
    function _zipMsg(html, cls) {
        var m=$('schZipMsg'); if(!m) return;
        m.innerHTML=html; m.className='sch-zip-msg '+(cls||'');
    }
    function _clearZipStatus() {
        _zipIcon(''); _zipMsg('');
        var el=$('schZip'); if(el){el.classList.remove('sch-zip-ok','sch-zip-err');}
    }
    function _showZipValid(autoAdvance) {
        var wasAlreadyValid = S.zipStatus==='valid';
        S.zipStatus='valid';
        _log('zip_valid',{zipcode:S.zip});
        _zipIcon('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1d9e75" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>');
        _zipMsg('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="vertical-align:-2px;margin-right:5px;"><path d="M5 13l4 4L19 7"/></svg>Great news \u2014 we serve your area!', 'sch-zip-msg--ok');
        var el=$('schZip'); if(el){el.classList.add('sch-zip-ok');el.classList.remove('sch-zip-err');}
        _updateNextBtn();
        // Auto-advance shortly after validating, so the user sees the confirmation first.
        // Skip if the zip was already valid before this call (e.g. re-rendering on back-nav).
        if (autoAdvance && !wasAlreadyValid && S.step===0) {
            var advanceSeq = S.zipSeq;
            setTimeout(function(){
                if (S.step===0 && S.zipStatus==='valid' && S.zipSeq===advanceSeq) {
                    S.step = nextStep(S.step); render();
                }
            }, 650);
        }
    }
    function _showZipInvalid(msg) {
        S.zipStatus='invalid';
        _log('zip_invalid',{zipcode:S.zip});
        _zipIcon('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c0381a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>');
        _zipMsg('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="vertical-align:-2px;margin-right:5px;"><path d="M18 6L6 18M6 6l12 12"/></svg>'+(msg||'Sorry, we don\u2019t serve that area yet.'), 'sch-zip-msg--err');
        var el=$('schZip'); if(el){el.classList.add('sch-zip-err');el.classList.remove('sch-zip-ok');}
        _updateNextBtn();
    }
    function _showZipChecking() {
        S.zipStatus='checking';
        _zipIcon('<span class="sch-spinner"></span>');
        _zipMsg('Checking your zip code\u2026', 'sch-zip-msg--checking');
        _updateNextBtn();
    }
    function _updateNextBtn() {
        if(S.step!==0) return;
        var n=$('schNext'); if(!n) return;
        var ok = S.zipStatus==='valid';
        n.disabled=!ok; n.style.opacity=ok?'1':'0.55';
    }
    function _triggerZipCheck() {
        if(ScheduledCfg.enableZipCheck===false){
            S.zipSeq++;
            _showZipValid(true);
            return;
        }
        var seq=++S.zipSeq;
        _showZipChecking();
        var body=new URLSearchParams();
        body.append('action','simply_scheduled_zip');
        body.append('nonce',ScheduledCfg.nonce);
        body.append('zipcode',S.zip);
        fetch(ScheduledCfg.ajaxUrl,{method:'POST',body:body})
            .then(function(r){return r.json();})
            .then(function(res){
                if(seq!==S.zipSeq) return;
                if(res&&res.success){
                    if(res.data&&res.data.valid){ _showZipValid(true); }
                    else { _showZipInvalid('Sorry, we don\u2019t serve that zip code yet. Call us at '+_phoneLinkHtml()+' and we\u2019ll help!'); }
                } else if(res&&res.data&&res.data.message) {
                    // Hard failure (e.g. auth error) — surface the message, block progress
                    _showZipInvalid(res.data.message);
                } else {
                    // Unknown API error — fail open so connectivity issues don't block bookings
                    _showZipValid(true);
                }
            })
            .catch(function(){
                if(seq!==S.zipSeq) return;
                _showZipValid(true); // fail open
            });
    }

    /* ----- Address-step zip validation (Service address section, separate from Location step) ----- */
    function _addrZipIcon(html) { var ic=$('schZipAIcon'); if(ic) ic.innerHTML=html; }
    function _addrZipMsg(html, cls) {
        var m=$('schZipAMsg'); if(!m) return;
        m.innerHTML=html; m.className='sch-zip-msg '+(cls||'');
    }
    function _showAddrZipValid() {
        S.zipAddrStatus='valid';
        _addrZipIcon('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1d9e75" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>');
        _addrZipMsg('', '');
        var el=$('schZipA'); if(el){el.classList.add('sch-zip-ok');el.classList.remove('sch-zip-err');}
    }
    function _showAddrZipInvalid(msg) {
        S.zipAddrStatus='invalid';
        _addrZipIcon('<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c0381a" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6L6 18M6 6l12 12"/></svg>');
        _addrZipMsg('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" style="vertical-align:-2px;margin-right:5px;"><path d="M18 6L6 18M6 6l12 12"/></svg>'+(msg||'Zip code is outside our service area.'), 'sch-zip-msg--err');
        var el=$('schZipA'); if(el){el.classList.add('sch-zip-err');el.classList.remove('sch-zip-ok');}
    }
    function _showAddrZipChecking() {
        S.zipAddrStatus='checking';
        _addrZipIcon('<span class="sch-spinner"></span>');
        _addrZipMsg('Checking zip code\u2026', 'sch-zip-msg--checking');
    }
    function _triggerAddrZipCheck() {
        if(ScheduledCfg.enableZipCheck===false){
            S.zipAddrSeq++;
            _showAddrZipValid();
            return;
        }
        var seq=++S.zipAddrSeq;
        _showAddrZipChecking();
        var body=new URLSearchParams();
        body.append('action','simply_scheduled_zip');
        body.append('nonce',ScheduledCfg.nonce);
        body.append('zipcode',S.zipAddr);
        fetch(ScheduledCfg.ajaxUrl,{method:'POST',body:body})
            .then(function(r){return r.json();})
            .then(function(res){
                if(seq!==S.zipAddrSeq) return;
                if(res&&res.success){
                    if(res.data&&res.data.valid){ _showAddrZipValid(); }
                    else { _showAddrZipInvalid('Zip code is outside our service area. Call us at '+_phoneLinkHtml()+' and we\u2019ll help!'); }
                } else if(res&&res.data&&res.data.message) {
                    _showAddrZipInvalid(res.data.message);
                } else {
                    // Unknown API error — fail open so connectivity issues don't block bookings
                    _showAddrZipValid();
                }
            })
            .catch(function(){
                if(seq!==S.zipAddrSeq) return;
                _showAddrZipValid(); // fail open
            });
    }

    var S = {
        step: 0, done: false, submitting: false,
        zip: '', zipStatus: 'idle', zipSeq: 0,
        first: '', last: '', phone: '', email: '',
        street: '', city: '', state: '', zipAddr: '', zipAddrStatus: 'idle', zipAddrSeq: 0,
        lookup: 'idle', foundAddr: null, foundAddrs: [], useFound: false, lookupSeq: 0,
        svc: '', jobType: '', detail: '', slot: '', notes: '',
        infoAnswers: {},
        uploads: [], // [{attachment_id, url, filename, uploading, error}]
        tab: 'first', calMonth: TODAY.getMonth(), calYear: TODAY.getFullYear(), calDate: null, calDateKey: null, availability: null, availabilityKey: null, slotsLoading: false, slotsError: ''
    };

    var GROUPS = [
        { label: 'Location', first: 0 },
        { label: 'Contact',  first: 1 },
        { label: 'Service',  first: 2 },
        { label: 'Schedule', first: 7 },
        { label: 'Review',   first: 8 }
    ];
    function groupOf(s) {
        if (s <= 0) return 0; if (s === 1) return 1;
        if (s <= 4) return 2; if (s <= 7) return 3; return 4;
    }

    var ICONS = {

        // ── General ──────────────────────────────────────────────────────
        wrench:         'M14.7 5.3a4.5 4.5 0 0 0-6 6L3 17v4h4l5.7-5.7a4.5 4.5 0 0 0 6-6l-2.9 2.9-2-2 2.9-2.9z',
        tools:          'M3 21l7-7m0 0l4-4m-4 4l-1.5-1.5M14 10l4-4M8 16l-5 5M21 3l-6 6M9 15l6-6',
        hammer:         'M13 4v4l3 3 4-4-3-3zM5 20l6-6M2 22l3-3',
        home:           'M3 11l9-8 9 8M5 10v10h14V10',
        shield:         'M12 2l8 4v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V6l8-4z',
        checkmark:      'M20 6L9 17l-5-5',
        clock:          'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 6v6l4 2',
        star:           'M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z',
        quote:          'M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2m-6 9l2 2 4-4',
        maintenance:    'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zm.5-14.5V12l3 3',
        repair:         'M14.7 5.3a4.5 4.5 0 0 0-6 6L3 17v4h4l5.7-5.7a4.5 4.5 0 0 0 6-6l-2.9 2.9-2-2 2.9-2.9z',
        leaf:           'M2 22c4-8 8-14 20-16-6 2-10 6-12 10 3-2 7-3 10-2-8 2-12 6-18 8z',
        spray:          'M3 3h4v4H3zM7 5h3M10 3l2 2-8 8-2-2 8-8zM14 8l2 2M16 14s0 4 4 4M18 10l4 4-4 4',
        tree:           'M12 2c-3 3-6 6-5 10h10c1-4-2-7-5-10zM12 12v10M9 22h6',

        // ── Plumbing ─────────────────────────────────────────────────────
        droplet:        'M12 3c-3 4-6 7-6 11a6 6 0 0012 0c0-4-3-7-6-11z',
        droplets:       'M7 4c-2 2.5-3 5-3 7a3 3 0 0 0 6 0c0-2-1-4.5-3-7zM17 4c-2 2.5-3 5-3 7a3 3 0 0 0 6 0c0-2-1-4.5-3-7zM9 18c0 2.5 1.5 3 3 3s3-.5 3-3',
        pipe:           'M4 12h16M4 8h4v8H4zM16 8h4v8h-4z',
        pipette:        'M2 22l7-7M14.5 2.5l7 7-7.5 7.5-7-7 7.5-7.5zM3.5 17.5l3 3',
        drain:          'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM12 8v8M8 12h8',
        valve:          'M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83',
        faucet:         'M5 8h8a2 2 0 0 1 2 2v1H5V8zM3 11h16v2H3zM7 13v5M11 13v5M15 13v5M5 18h12',
        water_heater:   'M8 3h8l1 5H7zM7 8v10a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V8M12 11v4M10 13h4',
        sewer:          'M3 3h18v4H3zM5 7v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7M9 11h6M9 15h6',
        toilet:         'M8 3h8v4H8zM6 7h12v3a6 6 0 0 1-12 0V7zM10 17v4M14 17v4M8 21h8',
        shower:         'M4 4h4v4H4zM8 6h4M12 3v6M10 9a8 8 0 0 1 8 8H2a8 8 0 0 1 8-8zM6 17v4M10 17v4M14 17v4',
        pump:           'M12 2a4 4 0 0 1 4 4v4H8V6a4 4 0 0 1 4-4zM8 10h8v2H8zM6 12h12v8a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2v-8z',

        // ── Electrical ───────────────────────────────────────────────────
        bolt:           'M13 2L4 14h6l-1 8 9-12h-6l1-8z',
        zap:            'M13 2L4 14h6l-1 8 9-12h-6l1-8z',
        plug:           'M12 22v-5M9 7V2M15 7V2M9 7h6a4 4 0 0 1 0 8H9a4 4 0 0 1 0-8z',
        outlet:         'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM9 9v2M15 9v2M9 15h6',
        switch:         'M5 9l2 3-2 3M19 9l-2 3 2 3M2 12h3M19 12h3M9 6h6M9 18h6',
        panel:          'M3 3h18v18H3zM3 9h18M3 15h18M9 3v18M15 3v18',
        circuit:        'M5 9H3M5 15H3M19 9h2M19 15h2M9 5V3M15 5V3M9 19v2M15 19v2M5 5m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0M19 5m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0M5 19m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0M19 19m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0M12 12m-3 0a3 3 0 1 0 6 0 3 3 0 1 0-6 0',
        lamp:           'M8 2h8l1 8H7zM12 10v5M9 22h6M10 15h4M10 19h4',
        battery:        'M7 7H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3M7 7V5a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v2M7 7h10M11 11v4M9 13h6',
        generator:      'M2 12h4l3-9 4 18 3-9h6',
        surge:          'M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z',
        ceiling_fan:    'M12 12m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0M12 2c0 4-2 6-2 6h4s-2-2-2-6zM12 22c0-4 2-6 2-6h-4s2 2 2 6zM2 12c4 0 6 2 6 2v-4s-2 2-6 2zM22 12c-4 0-6-2-6-2v4s2-2 6-2z',
        ev_charger:     'M14 2l-1 4h4l-5 8 1-5H9l5-7zM3 15h3v6H3zM18 15h3v6h-3z',

        // ── Heating ──────────────────────────────────────────────────────
        flame:          'M12 3c0 4-5 5.5-5 10a5 5 0 0 0 10 0c0-1.8-.8-3.2-1.8-4.7-.6 1-1.4 1.7-2.2 1.7C13.6 8.5 12 6 12 3z',
        thermometer:    'M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z',
        thermometer_up: 'M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0zM17 8l2-2 2 2M19 6v6',
        furnace:        'M3 3h18v6H3zM3 9h18v12H3zM7 9v12M12 9v12M17 9v12M7 6h.01M12 6h.01M17 6h.01',
        heat_wave:      'M3 8h18M3 12h18M3 16h18',
        radiator:       'M4 3h2v18H4zM9 3h2v18H9zM14 3h2v18h-2zM19 3h2v18h-2z',
        boiler:         'M7 3h10a2 2 0 0 1 2 2v5H5V5a2 2 0 0 1 2-2zM5 10h14v9a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-9zM9 14h.01M12 14h.01M15 14h.01',

        // ── Cooling ──────────────────────────────────────────────────────
        snowflake:      'M12 2v20M4 7l16 10M4 17L20 7',
        wind:           'M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2',
        air_vent:       'M6 12H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2M6 8h12M8 12v8M12 12v8M16 12v8',
        ac_unit:        'M2 9h20M2 15h20M9 3v18M15 3v18M3 3h18v18H3z',
        duct:           'M2 8h20v8H2zM6 8V6M10 8V4M14 8V6M18 8V4M6 16v2M10 16v4M14 16v2M18 16v4',
        coolant:        'M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83',
        compressor:     'M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20zM8 12h8M12 8v8',
        heat_pump:      'M3 17l2-5h14l2 5M1 21h22M5 12V7a7 7 0 0 1 14 0v5',
        fan:            'M12 12m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0M12 2c0 4-2 6-2 6h4s-2-2-2-6zM12 22c0-4 2-6 2-6h-4s2 2 2 6zM2 12c4 0 6 2 6 2v-4s-2 2-6 2zM22 12c-4 0-6-2-6-2v4s2-2 6-2z',
        filter:         'M3 5h18l-7 9v7l-4-2v-5L3 5z',
        refrigerant:    'M12 3a9 9 0 0 1 9 9h-4a5 5 0 0 0-5-5V3zM12 21a9 9 0 0 1-9-9h4a5 5 0 0 0 5 5v4z',

        // ── Roofing ──────────────────────────────────────────────────────
        roof:           'M2 12l10-9 10 9M5 12v9h14v-9',
        roof_shingle:   'M2 12l10-9 10 9M5 12v9h14v-9M5 15h4M10 12h4M15 15h4M8 18h8',
        gutter:         'M2 8h20v3H2zM5 11v8M19 11v8M5 19h14',
        chimney:        'M9 3h6v5H9zM7 8h10l2 13H5zM10 12h4M9 16h6',
        skylight:       'M2 12l10-9 10 9M5 12v9h14v-9M9 14h6v7H9z',
        hail:           'M2 12l10-9 10 9M5 12v9h14v-9M8 17h.01M12 15h.01M16 17h.01M10 19h.01M14 19h.01',
        solar:          'M2 12l10-9 10 9M5 12v9h14v-9M7 15h10M7 18h10',
        hard_hat:       'M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2zM10 10V5a2 2 0 0 1 4 0v5M4 15c0-4.4 3.6-8 8-8s8 3.6 8 8',

        // ── Garage Doors ─────────────────────────────────────────────────
        garage:         'M3 7h18v14H3zM3 7l9-5 9 5M9 21v-6h6v6M7 11h2M15 11h2M7 14h2M15 14h2',
        door:           'M5 3h14a1 1 0 0 1 1 1v17H4V4a1 1 0 0 1 1-1zm7 8a1 1 0 1 0 2 0 1 1 0 0 0-2 0z',
        garage_open:    'M3 7h18v14H3zM3 7l9-5 9 5M7 11h10M7 14h10M7 17h10',
        spring:         'M5 5c2-2 4-2 6 0s4 2 6 0M5 10c2-2 4-2 6 0s4 2 6 0M5 15c2-2 4-2 6 0s4 2 6 0M5 20c2-2 4-2 6 0s4 2 6 0',
        opener:         'M12 2a10 10 0 0 1 10 10H2A10 10 0 0 1 12 2zM2 12h20v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-8zM9 16h6',
        remote:         'M6 2h12a2 2 0 0 1 2 2v16a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zM9 7h6M9 11h6M9 15h2'
    };

    var SVCS = [], JOBTYPES = {}, DETAILS = {};

    var DEFAULT_DATA = {
        cats: [
            { n: 'Heating & cooling', d: 'AC, furnace, heat pumps',      i: ICONS.snowflake },
            { n: 'Plumbing',          d: 'Leaks, drains, water heaters', i: ICONS.droplet   },
            { n: 'Electrical',        d: 'Panels, outlets, lighting',    i: ICONS.bolt      }
        ],
        jt: {
            'Heating & cooling': [
                { n: 'Repair',                   i: ICONS.repair,       desc: 'Fix a broken system'    },
                { n: 'Maintenance',              i: ICONS.maintenance,  desc: 'Tune-up & inspection'   },
                { n: 'Install or replace quote', i: ICONS.quote,        desc: 'New equipment estimate' }
            ],
            'Plumbing': [
                { n: 'Repair',                   i: ICONS.repair, desc: 'Fix leaks, clogs & more'   },
                { n: 'Install or replace quote', i: ICONS.quote,  desc: 'New fixtures or equipment'  }
            ],
            'Electrical': [
                { n: 'Repair',                   i: ICONS.repair, desc: 'Fix outlets, panels & more' },
                { n: 'Install or replace quote', i: ICONS.quote,  desc: 'New wiring or equipment'    }
            ]
        },
        det: {
            'Heating & cooling': {
                'Repair':                   ['AC repair','Furnace repair','Repair ducts & vents','Repair heating system','Repair HVAC','Repair thermostat'],
                'Maintenance':              ['AC maintenance','Heating maintenance','HVAC maintenance'],
                'Install or replace quote': ['Install AC','Install ducts & vents','Install heating system','Install thermostat']
            },
            'Plumbing': {
                'Repair':                   ['Find & repair leak','Repair faucet','Repair garbage disposal','Repair pipe','Repair sewer','Repair toilet','Repair water heater','Unclog drain'],
                'Install or replace quote': ['Install faucet','Install garbage disposal','Install shower','Install toilet','Install water heater']
            },
            'Electrical': {
                'Repair':                   ['Repair light fixtures','Repair outlets or switches','Repair panel','Restore power'],
                'Install or replace quote': ['Install electric car charger','Install fan','Install ground wire','Install light fixtures','Install outdoor lighting','Install outlets or switches','Install security system','Relocate outlets or switches','Remodeling','Replace or upgrade panel']
            }
        }
    };

    // Build from PHP config if it has proper job types; otherwise use hardcoded defaults
    var cfgSvcs = (ScheduledCfg.services || []).filter(function(s){ return s && s.name; });
    var hasJtConfig = cfgSvcs.some(function(s){ return s.jobTypes && s.jobTypes.length > 0; });

    if (cfgSvcs.length && hasJtConfig) {
        cfgSvcs.forEach(function(s) {
            SVCS.push({ n: s.name, d: s.desc || '', i: ICONS[s.icon] || ICONS.wrench });
            JOBTYPES[s.name] = (s.jobTypes || []).map(function(jt) {
                return { n: jt.name, i: ICONS[jt.icon] || ICONS.wrench, desc: jt.desc || '' };
            });
            DETAILS[s.name] = {};
            (s.jobTypes || []).forEach(function(jt) {
                DETAILS[s.name][jt.name] = (jt.details || []).filter(Boolean);
            });
            // Also handle flat details (no job types on this category)
            if (!(s.jobTypes && s.jobTypes.length) && s.details && s.details.length) {
                JOBTYPES[s.name] = [];
                DETAILS[s.name][''] = s.details.filter(Boolean);
            }
        });
    } else {
        SVCS     = DEFAULT_DATA.cats;
        JOBTYPES = DEFAULT_DATA.jt;
        DETAILS  = DEFAULT_DATA.det;
    }

    function getJobTypes(svc)       { return JOBTYPES[svc] || []; }
    function getDetails(svc, jt)   { return (DETAILS[svc] && DETAILS[svc][jt]) ? DETAILS[svc][jt] : []; }
    function hasJobTypes(svc)       { return getJobTypes(svc).length > 0; }
    function hasDetailItems(svc,jt) { return getDetails(svc, jt).length > 0; }

    var DAYS = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    var MONS = ['January','February','March','April','May','June','July','August','September','October','November','December'];

    function esc(s) {
        return String(s == null ? '' : s).replace(/[&<>"']/g, function(c) {
            return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
        });
    }
    function $(id) { return document.getElementById(id); }
    function fmtSlot(d,w) { return DAYS[d.getDay()]+', '+MONS[d.getMonth()].slice(0,3)+' '+d.getDate()+' \u00b7 '+w; }
    function firstSlots() {
        var out=[], d=new Date(TODAY); d.setDate(d.getDate()+1);
        while (out.length < 4 && d <= MAXD) {
            for (var i=0; i<WINDOWS.length && out.length<4; i++) out.push(fmtSlot(d, WINDOWS[i]));
            d.setDate(d.getDate()+1);
        }
        return out;
    }
    function fullAddr() {
        if (S.useFound && S.foundAddr) {
            var a = S.foundAddr;
            return [a.street, a.city, (a.state+' '+a.zipcode).trim()].filter(Boolean).join(', ');
        }
        return [S.street, S.city, (S.state+' '+S.zipAddr).trim()].filter(Boolean).join(', ');
    }
    function head(t,s,center) {
        $('schTitle').textContent=t; $('schSub').textContent=s;
        $('schTitle').classList.toggle('sch-center',!!center);
        $('schSub').classList.toggle('sch-center',!!center);
    }
    function hero(html) {
        var e=$('schHero');
        if(html){e.innerHTML=html;e.hidden=false;}else e.hidden=true;
    }
    function err(m) {
        var e=$('schErr');
        if(m){e.textContent=m;e.hidden=false;}else e.hidden=true;
    }

    var HOME_SVG = '<svg width="200" height="118" viewBox="0 0 200 118" role="img" aria-label="Home inside a service area"><ellipse cx="100" cy="96" rx="78" ry="13" fill="#f2f6f8"/><ellipse cx="100" cy="96" rx="56" ry="9" fill="none" stroke="#cfe6f2" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/><ellipse cx="100" cy="96" rx="78" ry="13" fill="none" stroke="#9bd9ef" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/><rect x="72" y="62" width="56" height="36" rx="3" fill="#16384a"/><path d="M64 66 L100 38 L136 66 Z" fill="#00a9e0"/><rect x="93" y="76" width="14" height="22" rx="2" fill="#e8a33d"/><rect x="78" y="70" width="11" height="10" rx="1.5" fill="#dbeefb"/><rect x="111" y="70" width="11" height="10" rx="1.5" fill="#dbeefb"/><rect x="119" y="46" width="7" height="14" fill="#16384a"/><path d="M100 6 c-7.2 0-13 5.6-13 12.6 0 9 13 21.4 13 21.4 s13-12.4 13-21.4 C113 11.6 107.2 6 100 6z" fill="#00a9e0"/><circle cx="100" cy="18.5" r="5" fill="#ffffff"/><g stroke="#9bd9ef" stroke-width="2.5" stroke-linecap="round"><line x1="38" y1="52" x2="46" y2="52"/><line x1="30" y1="62" x2="42" y2="62"/><line x1="154" y1="52" x2="162" y2="52"/><line x1="158" y1="62" x2="170" y2="62"/></g></svg>';
    if (ScheduledCfg.colors) {
        if (ScheduledCfg.colors.primary) HOME_SVG = HOME_SVG.split('#00a9e0').join(ScheduledCfg.colors.primary);
        if (ScheduledCfg.colors.ink)     HOME_SVG = HOME_SVG.split('#16384a').join(ScheduledCfg.colors.ink);
    }
    var CHECK_SVG = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>';

    function svgIcon(path, sz) {
        sz = sz || 22;
        return '<svg width="'+sz+'" height="'+sz+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="'+esc(path)+'"/></svg>';
    }

    /* ----- Progress bar ----- */
    function prog() {
        var cur=groupOf(S.step), html='';
        GROUPS.forEach(function(g,i) {
            var done=S.done||i<cur, active=!S.done&&i===cur;
            var cls=(active?'is-active':'')+(done?' is-done':'');
            html+='<button type="button" data-g="'+i+'" class="'+cls+'" '+(done&&!S.done?'':'disabled')+' aria-label="'+g.label+'">'
                +'<span class="sch-prog-label">'+g.label+'</span><span class="sch-prog-bar"></span></button>';
        });
        $('schProg').innerHTML=html;
        Array.prototype.forEach.call(document.querySelectorAll('#schProg button:not([disabled])'), function(b) {
            b.addEventListener('click', function() { S.step=GROUPS[+b.dataset.g].first; render(); });
        });
    }
    function promise() {
        $('schPromise').innerHTML = S.done
            ? CHECK_SVG+' All set'
            : '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v4.7l3 1.8"/></svg> Takes about a minute';
    }

    /* ----- Field helpers ----- */
    function inputHtml(id,ph,val,type) {
        return '<input id="'+id+'" type="'+(type||'text')+'" placeholder="'+esc(ph)+'" value="'+esc(val)+'" autocomplete="off">';
    }
    function labelHtml(t,opt) {
        return '<label class="sch-label">'+t+(opt?' <span class="sch-opt">(optional)</span>':'')+  '</label>';
    }
    function sectionHtml(num,title,inner) {
        return '<div class="sch-section"><div class="sch-section-head"><span class="sch-section-num">'+num+'</span><span class="sch-section-title">'+esc(title)+'</span></div>'+inner+'</div>';
    }
    function slotHtml(value,label,selected) {
        return '<button type="button" class="sch-slot'+(selected?' is-selected':'')+'" data-s="'+esc(value)+'">'
            +'<span class="sch-radio">'+(selected?'<span class="sch-radio-dot"></span>':'')+'</span>'+esc(label)+'</button>';
    }

    /* ----- Job type card (large icon + name + description) ----- */
    function jobCard(jt, selected) {
        return '<button type="button" class="sch-jt-card'+(selected?' is-selected':'')+'" data-jt="'+esc(jt.n)+'">'
            +'<span class="sch-jt-icon">'+svgIcon(jt.i, 28)+'</span>'
            +'<span class="sch-jt-name">'+esc(jt.n)+'</span>'
            +(jt.desc?'<span class="sch-jt-desc">'+esc(jt.desc)+'</span>':'')
            +'</button>';
    }

    /* ----- Detail tile (compact grid) ----- */
    function detailTile(d, selected) {
        return '<button type="button" class="sch-tile'+(selected?' is-selected':'')+'" data-d="'+esc(d)+'">'+esc(d)+'</button>';
    }

    /* ----- Phone lookup ----- */
    var _nameLookupT=null;
    function _debouncedNameLookup() {
        var digits=S.phone.replace(/\D/g,'');
        if(digits.length!==10) return;
        if(!S.first.trim()||!S.last.trim()) return;
        clearTimeout(_nameLookupT);
        _nameLookupT=setTimeout(function(){ lookupPhone(digits); },500);
    }
    function lookupPhone(digits) {
        var seq=++S.lookupSeq;
        S.lookup='searching'; S.foundAddr=null; S.foundAddrs=[]; S.useFound=false;
        updateAddrZone(); updatePhoneIcon();
        var body=new URLSearchParams();
        body.append('action','simply_scheduled_lookup');
        body.append('nonce',ScheduledCfg.nonce);
        body.append('phone',digits);
        body.append('firstName',S.first||'');
        body.append('lastName',S.last||'');
        fetch(ScheduledCfg.ajaxUrl,{method:'POST',body:body})
            .then(function(r){return r.json();})
            .then(function(res){
                if(seq!==S.lookupSeq) return;
                if(res&&res.success&&res.data&&res.data.found&&res.data.addresses&&res.data.addresses.length){
                    S.foundAddrs=res.data.addresses;
                    S.foundAddr=res.data.addresses[0];
                    S.lookup='found'; S.useFound=true;
                    _log('phone_lookup',{found:'true',address_count:String(res.data.addresses.length),phone:digits,first:S.first,last:S.last});
                } else {
                    S.lookup='none';
                    _log('phone_lookup',{found:'false',phone:digits,first:S.first,last:S.last});
                }
                updateAddrZone(); updatePhoneIcon();
            })
            .catch(function(){
                if(seq!==S.lookupSeq) return;
                S.lookup='none'; updateAddrZone(); updatePhoneIcon();
            });
    }
    function updatePhoneIcon() {
        var ic=$('schPhIcon'); if(!ic) return;
        if(S.lookup==='searching') ic.innerHTML='<span class="sch-spinner"></span>';
        else if(S.lookup==='found') ic.innerHTML='<span style="color:#1d9e75;display:flex;">'+CHECK_SVG+'</span>';
        else ic.innerHTML='';
    }
    /* ----- Google Places Autocomplete (Street address field) ----- *
     * Uses the Places Autocomplete REST API directly instead of the
     * PlaceAutocompleteElement web component, giving full control over
     * styling and eliminating the mobile-sheet / dark-mode issues.
     * ----------------------------------------------------------------*/
    var _acSessionToken = null;
    var _acDebounceT = null;
    var _acReqSeq = 0;

    function _acGetKey() {
        // Key is not exposed in ScheduledCfg for security — we proxy through WP AJAX instead.
        return null; // key used server-side only; see ajax_places_autocomplete
    }

    function initStreetAutocomplete() {
        var mount = $('schStreetAuto');
        if (!mount) { console.warn('Simply Scheduled: #schStreetAuto not found'); return; }

        mount.innerHTML = '<label class="sch-label">Street address</label>'
            + '<div class="sch-ac-wrap">'
            + '<input id="schStreet" type="text" class="sch-ac-input" maxlength="100" placeholder="e.g. 123 Main St" value="'+esc(S.street)+'" autocomplete="off" aria-autocomplete="list" aria-expanded="false" aria-haspopup="listbox">'
            + '<div id="schAcDropdown" class="sch-ac-dropdown" role="listbox" hidden></div>'
            + '</div>';

        var inp = $('schStreet');
        var drop = $('schAcDropdown');
        if (!inp) return;

        inp.addEventListener('input', function() {
            S.street = inp.value;
            var q = inp.value.trim();
            if (q.length < 3) { _acHideDropdown(drop, inp); return; }
            clearTimeout(_acDebounceT);
            _acDebounceT = setTimeout(function(){ _acFetch(q, inp, drop); }, 220);
        });

        inp.addEventListener('blur', function(){
            // Small delay so click on suggestion fires before hiding
            setTimeout(function(){ _acHideDropdown(drop, inp); }, 180);
        });

        inp.addEventListener('keydown', function(e){
            var items = drop.querySelectorAll('.sch-ac-item');
            var active = drop.querySelector('.sch-ac-item--active');
            var idx = -1;
            items.forEach(function(el,i){ if(el===active) idx=i; });
            if(e.key==='ArrowDown'){
                e.preventDefault();
                var next = items[idx+1] || items[0];
                if(next){ if(active) active.classList.remove('sch-ac-item--active'); next.classList.add('sch-ac-item--active'); }
            } else if(e.key==='ArrowUp'){
                e.preventDefault();
                var prev = items[idx-1] || items[items.length-1];
                if(prev){ if(active) active.classList.remove('sch-ac-item--active'); prev.classList.add('sch-ac-item--active'); }
            } else if(e.key==='Enter'&&active){
                e.preventDefault();
                active.click();
            } else if(e.key==='Escape'){
                _acHideDropdown(drop, inp);
            }
        });
    }

    function _acHideDropdown(drop, inp) {
        if(drop){ drop.hidden=true; drop.innerHTML=''; }
        if(inp) inp.setAttribute('aria-expanded','false');
    }

    function _acFetch(query, inp, drop) {
        var seq = ++_acReqSeq;
        var body = new URLSearchParams();
        body.append('action', 'simply_scheduled_places');
        body.append('nonce', ScheduledCfg.nonce);
        body.append('query', query);
        fetch(ScheduledCfg.ajaxUrl, {method:'POST', body:body})
            .then(function(r){ return r.json(); })
            .then(function(res){
                if(seq !== _acReqSeq) return; // stale
                if(res.data && res.data._error) console.warn('Simply Scheduled Places API error:', res.data._error);
                if(!res.success || !res.data || !res.data.suggestions || !res.data.suggestions.length) { _acHideDropdown(drop, inp); return; }
                _acShowDropdown(res.data.suggestions, inp, drop);
            })
            .catch(function(){ _acHideDropdown(drop, inp); });
    }

    function _acShowDropdown(suggestions, inp, drop) {
        if(!suggestions.length){ _acHideDropdown(drop, inp); return; }
        drop.innerHTML = suggestions.map(function(s,i){
            return '<div class="sch-ac-item" role="option" data-place-id="'+esc(s.place_id||'')+'" data-description="'+esc(s.description||s.text||'')+'">'
                + '<span class="sch-ac-icon"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg></span>'
                + '<span>'+esc(s.description||s.text||'')+'</span>'
                + '</div>';
        }).join('');
        drop.hidden = false;
        inp.setAttribute('aria-expanded','true');

        Array.prototype.forEach.call(drop.querySelectorAll('.sch-ac-item'), function(item){
            item.addEventListener('mousedown', function(e){ e.preventDefault(); }); // prevent blur before click
            item.addEventListener('click', function(){
                var desc = item.dataset.description;
                var placeId = item.dataset.placeId;
                inp.value = desc;
                S.street = desc;
                _acHideDropdown(drop, inp);
                if(placeId) _acFetchDetails(placeId, inp);
            });
        });
    }

    function _acFetchDetails(placeId, inp) {
        var body = new URLSearchParams();
        body.append('action','simply_scheduled_place_detail');
        body.append('nonce',ScheduledCfg.nonce);
        body.append('place_id',placeId);
        fetch(ScheduledCfg.ajaxUrl,{method:'POST',body:body})
            .then(function(r){return r.json();})
            .then(function(res){
                if(!res.success||!res.data) return;
                var d=res.data;
                if(d.street) { S.street=d.street; if(inp) inp.value=d.street; }
                if(d.city) S.city=d.city;
                // Accept whatever state the address lookup returns — no longer forced to MN.
                if(d.state) S.state=d.state;
                var zipChanged = d.zip && d.zip!==S.zipAddr;
                if(d.zip) S.zipAddr=d.zip;
                render();
                if(zipChanged && S.zipAddr.length===5) _triggerAddrZipCheck();
                var cityEl=$('schCity'); if(cityEl) cityEl.focus();
            })
            .catch(function(){});
    }

    function updateAddrZone() {
        var z=$('schAddrZone'); if(!z) return;
        var FSC='width:100%;box-sizing:border-box;padding:12px 14px;border:1px solid #d4dde2;border-radius:10px;font-size:15px;color:#16384a;background:#ffffff;outline:none;font-family:inherit;color-scheme:light;';
        if(S.lookup==='idle'){
            z.innerHTML='<div class="sch-lookup-hint"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.35-4.35"/></svg>Enter your phone number above \u2014 if you\u2019ve worked with us before, we\u2019ll find your address automatically.</div>';
            return;
        }
        if(S.lookup==='searching'){
            z.innerHTML='<div class="sch-lookup-searching"><span class="sch-spinner"></span>Looking up your account\u2026</div>';
            return;
        }
        if(S.lookup==='found'&&S.useFound&&S.foundAddr){
            var a=S.foundAddr;
            var multiHtml='';
            if(S.foundAddrs.length>1){
                multiHtml='<div style="margin-top:10px;"><div style="font-size:12px;color:#46606f;font-weight:500;margin-bottom:6px;">Choose your address:</div>'
                    +S.foundAddrs.map(function(addr,i){
                        var sel=S.foundAddr===addr;
                        return '<button type="button" class="sch-addr-opt'+(sel?' is-selected':'')+'" data-idx="'+i+'">'
                            +'<span class="sch-addr-opt-street">'+esc(addr.street)+'</span>'
                            +'<span class="sch-addr-opt-city">'+esc(addr.city)+', '+esc(addr.state)+' '+esc(addr.zipcode)+'</span>'
                            +'</button>';
                    }).join('')+'</div>';
            }
            z.innerHTML='<div class="sch-found">'
                +'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1d9e75" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;margin-top:1px;"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg>'
                +'<div style="flex:1;"><div class="sch-found-eyebrow">WELCOME BACK \u2014 WE FOUND YOUR ADDRESS</div>'
                +(S.foundAddrs.length===1?'<div class="sch-found-street">'+esc(a.street)+'</div><div class="sch-found-city">'+esc(a.city)+', '+esc(a.state)+' '+esc(a.zipcode)+'</div>':'')
                +multiHtml
                +'<button type="button" class="sch-found-edit" id="schAddrEdit">Not your address? Enter a different one</button></div></div>';
            Array.prototype.forEach.call(z.querySelectorAll('.sch-addr-opt'),function(btn){
                btn.addEventListener('click',function(e){e.stopPropagation();S.foundAddr=S.foundAddrs[+btn.dataset.idx];updateAddrZone();});
            });
            $('schAddrEdit').addEventListener('click', function() { S.useFound=false; updateAddrZone(); });
            return;
        }
        if(!S.zipAddr&&S.zip) S.zipAddr=S.zip;
        var streetFieldHtml = ScheduledCfg.googleMapsEnabled
            ? '<div class="sch-field"><div id="schStreetAuto"></div></div>'
            : '<div class="sch-field">'+labelHtml('Street address')+'<input id="schStreet" type="text" maxlength="100" placeholder="e.g. 123 Main St" value="'+esc(S.street)+'" style="'+FSC+'" autocomplete="off"></div>';
        z.innerHTML=(S.lookup==='none'?'<div class="sch-notfound">No account found for that number \u2014 no problem, just enter your address.</div>':'')
            +streetFieldHtml
            +'<div class="sch-row-csz">'
            +'<div>'+labelHtml('City')+'<input id="schCity" type="text" placeholder="e.g. Thousand Oaks" value="'+esc(S.city)+'" style="'+FSC+'" autocomplete="off"></div>'
            +'<div>'+labelHtml('State')+'<input id="schState" type="text" maxlength="2" placeholder="e.g. CA" value="'+esc(S.state)+'" style="'+FSC+' text-transform:uppercase;" autocomplete="off"></div>'
            +'<div>'+labelHtml('Zip')
            +'<div class="sch-zip-wrap"><input id="schZipA" type="tel" maxlength="5" placeholder="e.g. 91362" value="'+esc(S.zipAddr)+'" style="'+FSC+'"><span class="sch-zip-icon" id="schZipAIcon"></span></div>'
            +'</div>'
            +'</div>'
            +'<div class="sch-zip-msg" id="schZipAMsg"></div>';
        if (ScheduledCfg.googleMapsEnabled) {
            setTimeout(function(){ initStreetAutocomplete(); }, 0);
        } else {
            $('schStreet').addEventListener('input',function(e){S.street=e.target.value;});
        }
        $('schCity').addEventListener('input',function(e){S.city=e.target.value;});
        // Reflect whatever the user types/selects for state — no forced default to MN.
        $('schState').addEventListener('input',function(e){
            e.target.value = e.target.value.toUpperCase();
            S.state=e.target.value;
        });
        var zipAEl = $('schZipA');
        zipAEl.setAttribute('autocomplete','off');
        if (S.zipAddrStatus==='valid') _showAddrZipValid();
        else if (S.zipAddrStatus==='invalid') _showAddrZipInvalid();
        zipAEl.addEventListener('input',function(e){
            e.target.value=e.target.value.replace(/\D/g,'');
            S.zipAddr=e.target.value;
            S.zipAddrStatus='idle'; S.zipAddrSeq=(S.zipAddrSeq||0);
            var icon=$('schZipAIcon'); if(icon) icon.innerHTML='';
            var msg=$('schZipAMsg'); if(msg){msg.innerHTML='';msg.className='sch-zip-msg';}
            e.target.classList.remove('sch-zip-ok','sch-zip-err');
            if(S.zipAddr.length===5) _triggerAddrZipCheck();
        });
    }

    /* ----- Calendar ----- */
    function calendarHtml() {
        var y=S.calYear, m=S.calMonth;
        var firstDow=new Date(y,m,1).getDay(), nDays=new Date(y,m+1,0).getDate();
        var prevOk=new Date(y,m,1)>new Date(TODAY.getFullYear(),TODAY.getMonth(),1);
        var nextOk=new Date(y,m+1,1)<=MAXD;
        var cells='';
        for(var i=0;i<firstDow;i++) cells+='<span></span>';
        for(var d=1;d<=nDays;d++){
            var dt=new Date(y,m,d), ok=dt>TODAY&&dt<=MAXD, sel=S.calDate&&dt.getTime()===S.calDate.getTime();
            cells+='<button type="button" data-day="'+d+'"'+(ok?'':' disabled')+(sel?' class="is-selected"':'')+'>'+d+'</button>';
        }
        return '<div class="sch-cal"><div class="sch-cal-head">'
            +'<button type="button" class="sch-cal-nav" id="schCalPrev"'+(prevOk?'':' disabled')+'><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button>'
            +'<span class="sch-cal-month">'+MONS[m]+' '+y+'</span>'
            +'<button type="button" class="sch-cal-nav" id="schCalNext"'+(nextOk?'':' disabled')+'><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button></div>'
            +'<div class="sch-cal-dows">'+DAYS.map(function(d){return '<span>'+d.toUpperCase().slice(0,2)+'</span>';}).join('')+'</div>'
            +'<div class="sch-cal-grid">'+cells+'</div></div>'
            +'<div class="sch-cal-legend"><span class="sch-cal-legend-dot"></span>Available dates</div>';
    }

    /* Map our category name to the API jobtype key */
    function svcToJobtype(svc) {
        var m={'heating & cooling':'hvac','plumbing':'plumbing','electrical':'electrical'};
        return m[svc.toLowerCase().trim()] || 'hvac';
    }

    /* Build the full selection chain for the API, e.g. ["Heating & Cooling","Repair","AC repair"] */
    function queryTypeChain() {
        return [S.svc, S.jobType, S.detail].filter(function(v){ return v && v.trim(); });
    }

    /* Fetch real availability from the API, cache in S.availability */
    function fetchSlots(cb) {
        var chainKey = queryTypeChain().join('|') + '|' + (S.zip||'');
        if(S.availability && S.availabilityKey===chainKey){ cb(); return; }
        if(!S.svc){
            // Safety net — should never happen by step 5, but never send an empty query_type
            S.slotsLoading=false;
            S.slotsError='Please select a service first.';
            S.availability=[];
            cb();
            return;
        }
        S.slotsLoading=true; S.slotsError='';
        var body=new URLSearchParams();
        body.append('action','simply_scheduled_slots');
        body.append('nonce',ScheduledCfg.nonce);
        body.append('jobtype',svcToJobtype(S.svc));
        body.append('query_type',JSON.stringify(queryTypeChain()));
        body.append('zipcode',S.zip||'');
        fetch(ScheduledCfg.ajaxUrl,{method:'POST',body:body})
            .then(function(r){return r.json();})
            .then(function(res){
                S.slotsLoading=false;
                if(res&&res.success&&res.data&&res.data.availability){
                    S.availability=res.data.availability;
                    S.availabilityKey=chainKey;
                } else {
                    S.slotsError=(res&&res.data&&res.data.message)||'Could not load availability.';
                    S.availability=[];
                }
                cb();
            })
            .catch(function(){
                S.slotsLoading=false;
                S.slotsError='Connection error. Please try again.';
                S.availability=[];
                cb();
            });
    }

    /* Format "2026-06-12" into "Thu, Jun 12" */
    function formatDate(dateStr) {
        var parts=dateStr.split('-');
        var d=new Date(+parts[0], +parts[1]-1, +parts[2]);
        return DAYS[d.getDay()]+', '+MONS[d.getMonth()].slice(0,3)+' '+d.getDate();
    }

    /* Build a slot value string from date + time range */
    function makeSlotVal(dateStr, time) {
        return formatDate(dateStr)+' \u00b7 '+time;
    }

    /* ----- Information step (optional) ----- */
    var INFO_QUESTIONS = [
        { key: 'home_age',        q: 'What is the age of your home?', options: ['0-10 Years','10+ Years','Not Sure'] },
        { key: 'system_working',  q: 'Is your system working?', options: ['Yes','No'] },
        { key: 'system_type',     q: 'What is the type of your system?', options: ['Gas','Electric','Not Sure'] },
        { key: 'authorized',      q: 'Do you own the home or are you authorized to have work done on the home?', options: ['Yes','No'] },
        { key: 'installed_by_us', q: 'Was the system installed by us?', options: ['Yes','No'] },
        { key: 'property_type',   q: 'Is it Residential or Commercial?', options: ['Residential','Commercial'] }
    ];
    // Answers that should hard-stop the booking flow — user must call instead of continuing.
    var INFO_BLOCKING_ANSWERS = {
        'property_type': ['Commercial']
    };
    // Answers that show an informational notice but do NOT block continuing.
    var INFO_NOTICE_ANSWERS = {
        'authorized': ['No']
    };
    function activeInfoQuestions() {
        var cfg       = ScheduledCfg.infoQuestions  || {};
        var customQs  = ScheduledCfg.customQuestions || [];
        var curDetail  = (S.detail  || '').trim();
        var curJobType = (S.jobType || '').trim();

        function appliesToCurrent(items) {
            if (!items || items.length === 0) return true;
            return items.some(function(it) {
                var t = (it || '').trim();
                return t === curDetail || t === curJobType;
            });
        }

        var active = INFO_QUESTIONS.filter(function(q) {
            var qcfg = cfg[q.key];
            if (!qcfg) return false;
            var enabled = (typeof qcfg === 'object') ? qcfg.enabled : !!qcfg;
            if (!enabled) return false;
            var items = (typeof qcfg === 'object' && Array.isArray(qcfg.items)) ? qcfg.items : [];
            return appliesToCurrent(items);
        });

        customQs.forEach(function(cq, idx) {
            if (!cq.question || !cq.options || !cq.options.length) return;
            if (!appliesToCurrent(cq.items)) return;
            active.push({ key: 'custom_' + idx, q: cq.question, options: cq.options });
        });

        return active;
    }
    function _infoBlockReason() {
        if (ScheduledCfg.blockCommercialBooking === false) return null;
        for (var key in INFO_BLOCKING_ANSWERS) {
            if (INFO_BLOCKING_ANSWERS.hasOwnProperty(key) && INFO_BLOCKING_ANSWERS[key].indexOf(S.infoAnswers[key]) !== -1) {
                return key;
            }
        }
        return null;
    }
    function _infoNoticeReasons() {
        var reasons = [];
        for (var key in INFO_NOTICE_ANSWERS) {
            if (INFO_NOTICE_ANSWERS.hasOwnProperty(key) && INFO_NOTICE_ANSWERS[key].indexOf(S.infoAnswers[key]) !== -1) {
                reasons.push(key);
            }
        }
        return reasons;
    }
    function _blockCallHtml() {
        return '<span>For this type of booking, please call <strong>'+_phoneLinkHtml()+'</strong> to complete your booking.</span>';
    }
    var INFO_NOTICE_TEXT = {
        'authorized': function(){ return ScheduledCfg.landlordNoticeText || '<p>Please note: To confirm your booking and dispatch a technician we will need your landlord confirmation.</p>'; }
    };
    function renderInfoStep(b) {
        var qs = activeInfoQuestions();
        if(!qs.length){
            // Nothing configured — auto-advance past this step
            S.step = nextStepAfterInfo(); render();
            return;
        }
        var html = qs.map(function(q,i){
            var opts = q.options.map(function(o){
                var checked = S.infoAnswers[q.key]===o;
                return '<label class="sch-radio-opt'+(checked?' is-selected':'')+'">'
                    +'<input type="radio" name="schInfo_'+q.key+'" value="'+esc(o)+'"'+(checked?' checked':'')+'> '+esc(o)+'</label>';
            }).join('');
            var noticeHtml = '';
            if (INFO_NOTICE_ANSWERS.hasOwnProperty(q.key) && INFO_NOTICE_ANSWERS[q.key].indexOf(S.infoAnswers[q.key]) !== -1) {
                var getText = INFO_NOTICE_TEXT[q.key];
                noticeHtml = '<div class="sch-info-notice">'+(getText ? getText() : '')+'</div>';
            }
            return '<div class="sch-info-block"><div class="sch-info-q">'+esc(q.q)+'</div><div class="sch-info-opts">'+opts+'</div>'+noticeHtml+'</div>';
        }).join('');

        var blockKey = _infoBlockReason();
        var blockHtml = blockKey ? '<div class="sch-info-blocked">'+_blockCallHtml()+'</div>' : '';

        b.innerHTML = '<div class="sch-info-list">'+html+'</div>'
            + blockHtml
            + (blockKey ? '' : (ScheduledCfg.allowSkipInfo && ScheduledCfg.allowSkipInfo !== '0' ? '<button type="button" id="schSkipInfo" class="sch-skip-btn">Skip this step</button>' : ''));

        Array.prototype.forEach.call(b.querySelectorAll('input[type=radio]'), function(r){
            r.addEventListener('change', function(e){
                var key = e.target.name.replace('schInfo_','');
                S.infoAnswers[key] = e.target.value;
                if (INFO_BLOCKING_ANSWERS.hasOwnProperty(key) && INFO_BLOCKING_ANSWERS[key].indexOf(e.target.value) !== -1) {
                    _log('info_blocked',{question:key,answer:e.target.value});
                }
                if (INFO_NOTICE_ANSWERS.hasOwnProperty(key) && INFO_NOTICE_ANSWERS[key].indexOf(e.target.value) !== -1) {
                    _log('info_notice_shown',{question:key,answer:e.target.value});
                }
                render();
            });
        });
        var skipBtn = $('schSkipInfo');
        if (skipBtn) skipBtn.addEventListener('click', function(){
            _log('info_step_skipped',{});
            S.step = nextStepAfterInfo(); render();
        });
    }

    /* ----- Upload step (optional) ----- */
    function renderUploadStep(b) {
        var items = S.uploads.map(function(u,i){
            if(u.uploading){
                return '<div class="sch-upload-item"><span class="sch-spinner"></span><span>'+esc(u.filename)+'</span></div>';
            }
            if(u.error){
                return '<div class="sch-upload-item sch-upload-item--error"><span>'+esc(u.filename)+' \u2014 '+esc(u.error)+'</span>'
                    +'<button type="button" class="sch-upload-remove" data-i="'+i+'">\u00d7</button></div>';
            }
            var isImg = /\.(jpe?g|png|gif|webp|heic)$/i.test(u.filename||'');
            return '<div class="sch-upload-item">'
                + (isImg && u.url ? '<img src="'+esc(u.url)+'" class="sch-upload-thumb" alt="">' : '<span class="sch-upload-file-icon">\ud83c\udfa5</span>')
                + '<span>'+esc(u.filename)+'</span>'
                + '<button type="button" class="sch-upload-remove" data-i="'+i+'">\u00d7</button></div>';
        }).join('');

        b.innerHTML = '<div class="sch-upload-zone" id="schUploadZone">'
            + '<input type="file" id="schUploadInput" accept="image/*,video/*" multiple style="display:none;">'
            + '<div class="sch-upload-cta"><span class="sch-upload-icon">\ud83d\udcf7</span><div>Tap to add photos or video</div><div class="sch-upload-hint">JPG, PNG, MP4, MOV \u00b7 up to 2MB each</div></div>'
            + '</div>'
            + (items ? '<div class="sch-upload-list">'+items+'</div>' : '')
            + '<button type="button" id="schSkipUpload" class="sch-skip-btn">Skip this step</button>';

        $('schUploadZone').addEventListener('click', function(){ $('schUploadInput').click(); });
        $('schUploadInput').addEventListener('change', function(e){
            var files = Array.prototype.slice.call(e.target.files||[]);
            files.forEach(uploadFile);
            e.target.value=''; // allow re-selecting the same file
        });
        Array.prototype.forEach.call(b.querySelectorAll('.sch-upload-remove'), function(btn){
            btn.addEventListener('click', function(){
                S.uploads.splice(+btn.dataset.i,1);
                render();
            });
        });
        $('schSkipUpload').addEventListener('click', function(){
            _log('upload_step_skipped',{});
            S.step = 7; render();
        });
    }
    var UPLOAD_MAX_BYTES = 2 * 1024 * 1024;
    function uploadFile(file) {
        if (file.size > UPLOAD_MAX_BYTES) {
            S.uploads.push({ filename: file.name, uploading: false, attachment_id: null, url: '', error: 'File is too large. Max size is 2MB.' });
            render();
            return;
        }
        var item = { filename: file.name, uploading: true, attachment_id: null, url: '', error: '' };
        S.uploads.push(item);
        render();
        var body = new FormData();
        body.append('action','simply_scheduled_upload');
        body.append('nonce',ScheduledCfg.nonce);
        body.append('file', file);
        fetch(ScheduledCfg.ajaxUrl,{method:'POST',body:body})
            .then(function(r){return r.json();})
            .then(function(res){
                item.uploading=false;
                if(res&&res.success){
                    item.attachment_id=res.data.attachment_id;
                    item.url=res.data.url;
                    item.filename=res.data.filename||item.filename;
                } else {
                    item.error=(res&&res.data&&res.data.message)||'Upload failed.';
                }
                render();
            })
            .catch(function(){
                item.uploading=false;
                item.error='Connection error.';
                render();
            });
    }

    function renderSchedule(b) {
        // Show loading state immediately, fetch then re-render body only
        if(S.slotsLoading){
            b.innerHTML='<div style="display:flex;align-items:center;gap:12px;padding:24px 0;justify-content:center;color:#6b7a85;font-size:14px;">'
                +'<span class="sch-spinner"></span>Loading availability\u2026</div>';
            return;
        }
        if(S.slotsError){
            b.innerHTML='<div style="padding:20px 0;text-align:center;">'
                +'<div style="color:#c0381a;font-size:13.5px;margin-bottom:14px;">'+esc(S.slotsError)+'</div>'
                +'<button type="button" id="schRetrySlots" style="padding:10px 20px;background:var(--sch-primary,#00a9e0);color:#fff;border:none;border-radius:8px;cursor:pointer;font-family:inherit;font-size:14px;font-weight:600;">Try again</button></div>';
            $('schRetrySlots').addEventListener('click',function(){
                S.availability=null; S.slotsError=''; S.slotsLoading=false;
                fetchSlots(function(){render();});
                S.slotsLoading=true; render();
            });
            b.innerHTML+='<div class="sch-field" style="margin-top:15px;">'+labelHtml('Notes',true)+'<textarea id="schNotes" rows="2" placeholder="Gate code, pets, where the problem is\u2026">'+esc(S.notes)+'</textarea></div>';
            if($('schNotes')) $('schNotes').addEventListener('input',function(e){S.notes=e.target.value;});
            return;
        }

        var avail=S.availability||[];

        /* Build "First available" = first 4 slots across all dates in order */
        var firstSlotsList=[];
        avail.forEach(function(day){
            day.times.forEach(function(t){
                if(firstSlotsList.length<4) firstSlotsList.push({v:makeSlotVal(day.date,t),l:t,date:day.date});
            });
        });

        /* Build "All appointments" - dates with available times */
        var dateSlots={};
        avail.forEach(function(day){dateSlots[day.date]=day.times;});
        var availDates=Object.keys(dateSlots);

        var inner='';
        if(S.tab==='first'){
            if(firstSlotsList.length===0){
                inner='<div class="sch-cal-empty-hint" style="padding:20px 0;">No upcoming availability found. Please call us at '+_phoneLinkHtml()+' to schedule.</div>';
            } else {
                inner='<div class="sch-kicker">First available</div><div class="sch-stack">'
                    +firstSlotsList.map(function(sl){return slotHtml(sl.v,formatDate(sl.date)+' \u00b7 '+sl.l,S.slot===sl.v);}).join('')+'</div>';
            }
        } else {
            // Calendar with only available dates enabled
            var y=S.calYear, m=S.calMonth;
            var firstDow=new Date(y,m,1).getDay(), nDays=new Date(y,m+1,0).getDate();
            var prevOk=new Date(y,m,1)>new Date(TODAY.getFullYear(),TODAY.getMonth(),1);
            var nextOk=new Date(y,m+1,1)<=MAXD;
            var cells='';
            for(var i=0;i<firstDow;i++) cells+='<span></span>';
            for(var d=1;d<=nDays;d++){
                var dateKey=(y+'-'+String(m+1).padStart(2,'0')+'-'+String(d).padStart(2,'0'));
                var hasSlots=!!(dateSlots[dateKey]&&dateSlots[dateKey].length);
                var sel=S.calDate&&(S.calYear+'-'+String(S.calMonth+1).padStart(2,'0')+'-'+String(S.calDate.getDate()).padStart(2,'0'))===dateKey;
                cells+='<button type="button" data-day="'+d+'" data-dkey="'+dateKey+'"'+(hasSlots?' data-avail="1"':' disabled')+(sel?' class="is-selected"':'')+'>'+d+'</button>';
            }
            inner='<div class="sch-cal"><div class="sch-cal-head">'
                +'<button type="button" class="sch-cal-nav" id="schCalPrev"'+(prevOk?'':' disabled')+'><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button>'
                +'<span class="sch-cal-month">'+MONS[m]+' '+y+'</span>'
                +'<button type="button" class="sch-cal-nav" id="schCalNext"'+(nextOk?'':' disabled')+'><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg></button></div>'
                +'<div class="sch-cal-dows">'+DAYS.map(function(d){return '<span>'+d.toUpperCase().slice(0,2)+'</span>';}).join('')+'</div>'
                +'<div class="sch-cal-grid">'+cells+'</div></div>'
            +'<div class="sch-cal-legend"><span class="sch-cal-legend-dot"></span>Available dates</div>';

            if(S.calDateKey&&dateSlots[S.calDateKey]){
                inner+='<div class="sch-kicker">Arrival window \u00b7 '+formatDate(S.calDateKey)+'</div>'
                    +'<div class="sch-grid-2">'+dateSlots[S.calDateKey].map(function(t){
                        var v=makeSlotVal(S.calDateKey,t);
                        return slotHtml(v,t,S.slot===v);
                    }).join('')+'</div>';
            } else if(availDates.length) {
                inner+='<div class="sch-cal-empty-hint">Pick a highlighted date to see arrival windows.</div>';
            }
        }

        b.innerHTML='<div class="sch-tabs">'
            +'<button type="button" class="sch-tab'+(S.tab==='first'?' is-active':'')+'" id="schTabF">First available</button>'
            +'<button type="button" class="sch-tab'+(S.tab==='all'?' is-active':'')+'" id="schTabA">All appointments</button></div>'
            +inner
            +'<div class="sch-field" style="margin-top:15px;">'+labelHtml('Notes',true)
            +'<textarea id="schNotes" rows="2" placeholder="Gate code, pets, where the problem is\u2026">'+esc(S.notes)+'</textarea></div>';

        $('schTabF').addEventListener('click',function(){S.tab='first';render();});
        $('schTabA').addEventListener('click',function(){S.tab='all';render();});
        Array.prototype.forEach.call(b.querySelectorAll('.sch-slot'),function(c){
            c.addEventListener('click',function(){S.slot=c.dataset.s;_log('slot_selected',{slot:S.slot,service:S.svc,tab:S.tab});render();});
        });
        var p=$('schCalPrev'), n=$('schCalNext');
        if(p&&!p.disabled) p.addEventListener('click',function(){S.calMonth--;if(S.calMonth<0){S.calMonth=11;S.calYear--;}render();});
        if(n&&!n.disabled) n.addEventListener('click',function(){S.calMonth++;if(S.calMonth>11){S.calMonth=0;S.calYear++;}render();});
        Array.prototype.forEach.call(b.querySelectorAll('.sch-cal-grid button:not([disabled])'),function(d){
            d.addEventListener('click',function(){
                S.calDateKey=d.dataset.dkey;
                S.calDate=new Date(S.calYear,S.calMonth,+d.dataset.day);
                S.slot=''; render();
            });
        });
        if($('schNotes')) $('schNotes').addEventListener('input',function(e){S.notes=e.target.value;});
    }

    /* ----- Main render ----- */
    function render() {
        prog(); promise(); err(''); hero(null);
        var b=$('schBody'), back=$('schBack'), next=$('schNext');
        b.className='sch-pane';
        back.hidden=!(S.step>0&&!S.done);
        next.hidden=false; next.disabled=false;
        next.textContent=S.step===8?'Confirm booking':'Continue';

        if(S.done){
            head('','');
            b.innerHTML='<div class="sch-success">'
                +'<div class="sch-success-icon"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg></div>'
                +'<div class="sch-success-title">You\u2019re booked!</div>'
                +'<div class="sch-success-text">We\u2019ll see you <strong>'+esc(S.slot)+'</strong>'
                +(S.email?' \u2014 confirmation sent to <strong>'+esc(S.email)+'</strong>':'')
                +'.<br><span style="font-size:13px;color:#8a98a3;">'+(ScheduledCfg.successText||'Your technician will text when they\u2019re on the way.')+'</span></div></div>';
            next.hidden=true; back.hidden=true; return;
        }

        /* Step 0 — Location */
        if(S.step===0){
            hero(HOME_SVG);
            head('Where are you?','Enter your Zip Code so we can check that we serve your area.',true);
            b.innerHTML='<div class="sch-field">'
                + labelHtml('Zip Code')
                + '<div class="sch-zip-wrap">'
                +   inputHtml('schZip','e.g. 55401',S.zip,'tel')
                +   '<span class="sch-zip-icon" id="schZipIcon"></span>'
                + '</div>'
                + '<div class="sch-zip-msg" id="schZipMsg"></div>'
                + '</div>';

            var el=$('schZip');
            el.maxLength=5;
            el.setAttribute('inputmode','numeric');

            // Restore prior validation state if user came back
            if(S.zipStatus==='valid')   _showZipValid();
            else if(S.zipStatus==='invalid') _showZipInvalid('Sorry, we don\u2019t serve that zip code yet.');

            el.addEventListener('input',function(e){
                e.target.value=e.target.value.replace(/\D/g,'');
                S.zip=e.target.value;
                S.zipStatus='idle'; S.zipSeq=(S.zipSeq||0);
                _clearZipStatus();
                _updateNextBtn();
                if(S.zip.length===5) _triggerZipCheck();
            });
            el.addEventListener('keydown',function(e){if(e.key==='Enter'&&S.zipStatus==='valid')$('schNext').click();});
            _updateNextBtn();
            setTimeout(function(){el.focus();},60);
        }

        /* Step 1 — Contact */
        else if(S.step===1){
            head('How can we reach you?','Your phone number lets us find your account instantly.');
            var s1='<div class="sch-row-2" style="margin-bottom:13px;">'
                +'<div>'+labelHtml('First name')+inputHtml('schFirst','e.g. Jane',S.first)+'</div>'
                +'<div>'+labelHtml('Last name')+inputHtml('schLast','e.g. Doe',S.last)+'</div></div>'
                +'<div class="sch-field">'+labelHtml('Mobile phone')
                +'<div class="sch-phone-wrap">'+inputHtml('schPhone','e.g. (555) 555-0123',S.phone,'tel')+'<span class="sch-phone-icon" id="schPhIcon"></span></div></div>'
                +'<div>'+labelHtml('Email',true)+inputHtml('schEmail','e.g. jane@example.com',S.email,'email')+'</div>';
            b.innerHTML=sectionHtml(1,'Your details',s1)+sectionHtml(2,'Service address','<div id="schAddrZone"></div>')
                +'<p class="sch-legal">'+(ScheduledCfg.legalText||'By booking, you agree to receive appointment confirmations and reminders by call, text, or email. Reply STOP anytime to opt out.')+'</p>';
            $('schFirst').addEventListener('input',function(e){S.first=e.target.value; _debouncedNameLookup();});
            $('schLast').addEventListener('input',function(e){S.last=e.target.value; _debouncedNameLookup();});
            $('schEmail').addEventListener('input',function(e){S.email=e.target.value;});
            $('schPhone').addEventListener('input',function(e){
                var v=e.target.value.replace(/\D/g,'').slice(0,10);
                if(v.length>6) e.target.value='('+v.slice(0,3)+') '+v.slice(3,6)+'-'+v.slice(6);
                else if(v.length>3) e.target.value='('+v.slice(0,3)+') '+v.slice(3);
                else e.target.value=v;
                S.phone=e.target.value;
                if(v.length===10){ if(S.first.trim()&&S.last.trim()) lookupPhone(v); }
                else if(S.lookup!=='idle'){ S.lookupSeq++; S.lookup='idle'; S.foundAddr=null; S.foundAddrs=[]; S.useFound=false; updateAddrZone(); updatePhoneIcon(); }
            });
            updateAddrZone(); updatePhoneIcon();
        }

        /* Step 2 — Category */
        else if(S.step===2){
            head('What do you need help with?','Pick a service category.');
            b.innerHTML='<div class="sch-stack">'+SVCS.map(function(s){
                var on=S.svc===s.n;
                return '<button type="button" class="sch-card'+(on?' is-selected':'')+'" data-n="'+esc(s.n)+'">'
                    +'<span class="sch-card-icon">'+svgIcon(s.i)+'</span>'
                    +'<span style="flex:1;"><span class="sch-card-name">'+esc(s.n)+'</span><span class="sch-card-desc">'+esc(s.d)+'</span></span></button>';
            }).join('')+'</div>';
            Array.prototype.forEach.call(b.querySelectorAll('.sch-card'),function(c){
                c.addEventListener('click',function(){
                    S.svc=c.dataset.n; S.jobType=''; S.detail='';
                    c.classList.add('is-selected');
                    _log('category_selected',{service:S.svc});
                    setTimeout(function(){ S.step=hasJobTypes(S.svc)?3:nextStepAfterService(); render(); },180);
                });
            });
            next.hidden=true;
        }

        /* Step 3 — Job type + detail inline (single combined screen) */
        else if(S.step===3){
            head('What Type of Service?', 'Select a Service Type, then pick a specific option.');
            var jts = getJobTypes(S.svc);
            var rows = jts.map(function(jt) {
                var isOpen = S.jobType === jt.n;
                var dets   = getDetails(S.svc, jt.n);
                var rowHtml = '<button type="button" class="sch-jt-row' + (isOpen ? ' is-open' : '') + '" data-jt="' + esc(jt.n) + '">'
                    + '<span class="sch-jt-icon">' + svgIcon(jt.i, 20) + '</span>'
                    + '<span class="sch-jt-text">'
                    +   '<span class="sch-jt-name">' + esc(jt.n) + '</span>'
                    +   (jt.desc ? '<span class="sch-jt-desc">' + esc(jt.desc) + '</span>' : '')
                    + '</span>'
                    + '<span class="sch-jt-chev"><svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg></span>'
                    + '</button>';

                if (isOpen && dets.length) {
                    rowHtml += '<div class="sch-det-panel">'
                        + '<div class="sch-det-label">Choose a specific service</div>'
                        + '<div class="sch-grid-auto">'
                        + dets.map(function(d) {
                            return '<button type="button" class="sch-tile sch-det-item' + (S.detail === d ? ' is-selected' : '') + '" data-d="' + esc(d) + '">' + esc(d) + '</button>';
                        }).join('')
                        + '</div></div>';
                } else if (isOpen && !dets.length) {
                    // Job type with no sub-items — selection is the job type itself
                    rowHtml += '<div class="sch-det-panel sch-det-confirm">'
                        + '<div style="display:flex;align-items:center;gap:8px;font-size:13.5px;color:#0f6e56;">'
                        + '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>'
                        + esc(jt.n) + ' selected'
                        + '</div></div>';
                }
                return rowHtml;
            }).join('');

            b.innerHTML = '<div class="sch-jt-list">' + rows + '</div>';

            Array.prototype.forEach.call(b.querySelectorAll('.sch-jt-row'), function(c) {
                c.addEventListener('click', function() {
                    var jtn = c.dataset.jt;
                    if (S.jobType === jtn) {
                        S.jobType = ''; S.detail = '';
                        render();
                    } else {
                        S.jobType = jtn; S.detail = '';
                        _log('jobtype_selected',{service:S.svc,job_type:jtn});
                        if (!hasDetailItems(S.svc, jtn)) {
                            // No further sub-items — this selection completes the step, auto-advance
                            S.detail = jtn;
                            render();
                            setTimeout(function(){ S.step = nextStep(S.step); render(); }, 180);
                        } else {
                            render();
                        }
                    }
                });
            });
            Array.prototype.forEach.call(b.querySelectorAll('.sch-det-item'), function(c) {
                c.addEventListener('click', function(e) {
                    e.stopPropagation();
                    S.detail = c.dataset.d;
                    c.classList.add('is-selected');
                    _log('detail_selected',{service:S.svc,job_type:S.jobType,detail:S.detail});
                    setTimeout(function(){ S.step = nextStep(S.step); render(); }, 180);
                });
            });
        }

        /* Step 4 — no longer used as standalone; kept for back-nav skip logic */
        else if(S.step===4){
            S.step = nextStepAfterService(); render(); return;
        }

        /* Step 5 — Information (optional) */
        else if(S.step===5){
            head('Tell us a bit more','This helps your technician prepare \u2014 totally optional.');
            renderInfoStep(b);
            if(_infoBlockReason()) next.hidden=true;
        }

        /* Step 6 — Upload photos/video (optional) */
        else if(S.step===6){
            head('Add photos or video','Show us the issue so we can come prepared \u2014 totally optional.');
            renderUploadStep(b);
        }

        /* Step 7 — Schedule — fetch real slots on first entry, then render */
        else if(S.step===7){
            head('Pick a time','Grab the first opening, or browse the full calendar.');
            var currentChainKey = [S.svc, S.jobType, S.detail].filter(function(v){return v&&v.trim();}).join('|') + '|' + (S.zip||'');
            var isStale = S.availabilityKey !== currentChainKey;
            if((!S.availability || isStale) && !S.slotsLoading){
                S.slotsLoading=true;
                renderSchedule(b); // show spinner immediately
                fetchSlots(function(){ render(); });
                return;
            }
            renderSchedule(b);
        }

        /* Step 8 — Review */
        else if(S.step===8){
            head('Confirm your appointment','Tap any completed step above to make changes.');
            function row(k,v){return '<div class="sch-review-row"><span class="sch-review-key">'+k+'</span><span class="sch-review-val">'+esc(v||'\u2014')+'</span></div>';}
            var svcLabel=S.svc+(S.jobType?' \u00b7 '+S.jobType:'')+(S.detail?' \u00b7 '+S.detail:'');
            b.innerHTML='<div class="sch-review">'
                +row('Name',S.first+' '+S.last)
                +row('Phone',S.phone)
                +(S.email?row('Email',S.email):'')
                +row('Service',svcLabel)
                +row('Address',fullAddr())
                +row('Arrival window',S.slot)+'</div>';
        }
    }

    /* Determine the next step after service selection, skipping disabled optional sections */
    function nextStepAfterService() {
        if(ScheduledCfg.enableInfoSection) return 5;
        if(ScheduledCfg.enableUploadSection) return 6;
        return 7;
    }
    function nextStepAfterInfo() {
        if(ScheduledCfg.enableUploadSection) return 6;
        return 7;
    }

    /* ----- Validation ----- */
    function validate() {
        if(S.step===0){
            if(S.zip.length<5) return 'Please enter a valid 5-digit zip code.';
            if(S.zipStatus==='checking') return 'One moment \u2014 checking your zip code.';
            if(S.zipStatus==='invalid') return 'Sorry, we don\u2019t serve that zip code yet.';
            if(S.zipStatus!=='valid') return 'Please enter a valid 5-digit zip code.';
        }
        if(S.step===1){
            if(!S.first.trim()||!S.last.trim()) return 'Please enter your first and last name.';
            if(S.phone.replace(/\D/g,'').length<10) return 'Please enter a valid 10-digit phone number.';
            if(S.lookup==='searching') return 'One moment \u2014 still looking up your account.';
            // Email is always optional — never block on it being empty
            if(S.email&&!/^\S+@\S+\.\S+$/.test(S.email)) return 'That email doesn\u2019t look right \u2014 fix it or leave it blank.';
            if(!(S.useFound&&S.foundAddr)){
                if(!S.street.trim()||!S.city.trim()||S.zipAddr.length<5) return 'Please complete your service address.';
                if(S.zipAddrStatus==='checking') return 'One moment \u2014 checking your zip code.';
                if(S.zipAddrStatus==='invalid') return 'Sorry, that zip code is outside our service area.';
            }
        }
        if(S.step===3){
            if(!S.jobType) return 'Please select a service type.';
            if(hasDetailItems(S.svc, S.jobType) && !S.detail) return 'Please choose a specific service.';
        }
        if(S.step===5&&_infoBlockReason()) return 'Please call us to complete this type of booking.';
        if(S.step===7&&!S.slot) return S.tab==='all'&&!S.calDate?'Please pick a date first, then an arrival window.':'Please choose an arrival window.';
        return '';
    }

    /* ----- Submit ----- */
    function submit() {
        if(S.submitting) return;
        S.submitting=true;
        var next=$('schNext');
        next.disabled=true; next.textContent='Booking\u2026';

        // Resolve address parts — prefer the structured found address,
        // fall back to what the user typed in the manual fields
        var addrStreet, addrCity, addrState, addrZipcode;
        if(S.useFound && S.foundAddr){
            addrStreet  = S.foundAddr.street  || '';
            addrCity    = S.foundAddr.city    || '';
            addrState   = S.foundAddr.state   || '';
            addrZipcode = S.foundAddr.zipcode || S.zip;
        } else {
            addrStreet  = S.street  || '';
            addrCity    = S.city    || '';
            addrState   = S.state   || '';
            addrZipcode = S.zipAddr || S.zip;
        }

        var body=new URLSearchParams();
        body.append('action','simply_scheduled_submit');
        body.append('nonce',ScheduledCfg.nonce);
        body.append('firstName',S.first);
        body.append('lastName',S.last);
        body.append('phone',S.phone);
        body.append('email',S.email);
        body.append('zip',S.zip);
        body.append('address',fullAddr());
        body.append('addrStreet',addrStreet);
        body.append('addrCity',addrCity);
        body.append('addrState',addrState);
        body.append('addrZipcode',addrZipcode);
        body.append('addressSource',S.useFound?'lookup':'manual');
        body.append('serviceType',S.svc);
        body.append('serviceDetail',[S.jobType,S.detail].filter(Boolean).join(' \u00b7 '));
        body.append('queryType',JSON.stringify([S.svc,S.jobType,S.detail].filter(function(v){return v&&v.trim();})));
        body.append('arrivalWindow',S.slot);
        body.append('notes',S.notes);
        body.append('infoAnswers',JSON.stringify(S.infoAnswers||{}));
        body.append('uploadedAttachmentIds',JSON.stringify(
            S.uploads.filter(function(u){return u.attachment_id&&!u.error;}).map(function(u){return u.attachment_id;})
        ));
        body.append('utmParams',JSON.stringify(_getUtm()));
        body.append('sessionId',_sid);

        fetch(ScheduledCfg.ajaxUrl,{method:'POST',body:body})
            .then(function(r){return r.json();})
            .then(function(res){
                S.submitting=false;
                if(res&&res.success){
                    _log('booking_submitted',{booking_id:res.data&&res.data.booking_id?String(res.data.booking_id):'',api_status:res.data&&res.data.api_status||'unknown',service:S.svc,job_type:S.jobType,slot:S.slot,phone:S.phone,email:S.email,first:S.first,last:S.last});
                    // Fire CallRail form submission event if enabled
                    if(ScheduledCfg.enableCallRail){
                        var _crPayload = {
                            form_name:    'Simply Scheduled Booking',
                            first_name:   S.first,
                            last_name:    S.last,
                            phone_number: S.phone,
                            email_address: S.email
                        };
                        try {
                            if(window.CallTrk && typeof window.CallTrk.formSubmitted==='function'){
                                // Full form-tracking snippet — preferred
                                window.CallTrk.formSubmitted(_crPayload);
                            } else {
                                // Fallback: push directly into CallRail's event queue
                                // Works with basic call-tracking snippet (no formSubmitted method needed)
                                window._ctq = window._ctq || [];
                                window._ctq.push(['trackSubmit', _crPayload]);
                            }
                        } catch(e) {
                            console.warn('[Simply Scheduled] CallRail tracking failed:', e);
                        }
                    }
                    S.done=true; render();
                }
                else {
                    next.disabled=false; next.textContent='Confirm booking';
                    err((res&&res.data&&res.data.message)||'Something went wrong. Please try again or give us a call.');
                }
            })
            .catch(function(){
                S.submitting=false;
                next.disabled=false; next.textContent='Confirm booking';
                err('Connection problem \u2014 please try again or give us a call.');
            });
    }

    /* ----- Button wiring ----- */
    $('schNext').addEventListener('click',function(){
        var m=validate(); if(m){ _log('validation_error',{step:String(S.step),error:m,phone:S.phone||'',first:S.first||'',last:S.last||''}); return err(m); }
        if(S.step===8) return submit();
        var stepLabels=['location','contact','category','service_type','service_detail','information','upload','schedule','review'];
        _logStep('step_completed',{from_step:String(S.step),from_name:stepLabels[S.step]||'unknown'});
        S.step=nextStep(S.step);
        render();
    });
    $('schBack').addEventListener('click',function(){
        S.step=prevStep(S.step);
        render();
    });

    /* Advance to the next step, skipping disabled optional sections */
    function nextStep(s) {
        if(s===4) return nextStepAfterService();
        if(s===5) return nextStepAfterInfo();
        if(s===6) return 7;
        return s+1;
    }
    /* Go back a step, skipping disabled optional sections and the no-op step 4 */
    function prevStep(s) {
        if(s===7){ // leaving Schedule backward
            if(ScheduledCfg.enableUploadSection) return 6;
            if(ScheduledCfg.enableInfoSection) return 5;
            return hasJobTypes(S.svc)?3:2;
        }
        if(s===6){ // leaving Upload backward
            if(ScheduledCfg.enableInfoSection) return 5;
            return hasJobTypes(S.svc)?3:2;
        }
        if(s===5){ // leaving Information backward
            return hasJobTypes(S.svc)?3:2;
        }
        if(s===3&&!hasJobTypes(S.svc)) return 2;
        return s-1;
    }

    function openModal() {
        // Measure scrollbar width before locking so body padding can compensate
        var scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
        document.documentElement.style.setProperty('--sch-scrollbar-width', scrollbarWidth + 'px');
        overlay.hidden = false;
        document.body.classList.add('scheduled-lock');
        _stepTs = Date.now();
        _log('modal_open', {referrer: document.referrer.slice(0,200) || 'direct'});
        render();
    }
    function _dispatchOpen() { document.dispatchEvent(new CustomEvent('simplyScheduled:open')); }
    function _dispatchClose(){ document.dispatchEvent(new CustomEvent('simplyScheduled:close')); }
    function closeModal() {
        overlay.hidden = true;
        document.body.classList.remove('scheduled-lock');
        try { _log('modal_close', {step: String(S.step), done: String(S.done)}); } catch(e) {}
        try { _dispatchClose(); } catch(e) {}
    }

    Array.prototype.forEach.call(document.querySelectorAll('.scheduled-open,.scheduled-trigger'),function(t){
        t.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();openModal();});
    });
    overlay.querySelector('.sch-close').addEventListener('click',function(e){
        e.stopPropagation();
        closeModal();
    });
    // NOTE: intentionally no backdrop-click-to-close handler here.
    // The popup should only close via the explicit close (X) button.

    function urlWantsOpen() {
        if(window.location.hash==='#scheduled') return true;
        try { var q=new URLSearchParams(window.location.search).get('scheduled'); return q==='open'||q==='1'||q==='true'; } catch(e){ return false; }
    }
    if(urlWantsOpen()) openModal();
    window.addEventListener('hashchange',function(){if(window.location.hash==='#scheduled')openModal();});
    document.addEventListener('simplyScheduled:open',openModal);
    // NOTE: do NOT add a listener for 'simplyScheduled:close' here — closeModal already
    // dispatches that event for external consumers; listening to it internally causes
    // infinite recursion (closeModal → _dispatchClose → closeModal → ...).
})();