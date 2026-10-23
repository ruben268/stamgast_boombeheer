/* =========================================================
   Cookiemelding + Google Consent Mode v2 + Google Tag Manager
   Stamgast Boombeheer

   - Google Tag Manager wordt PAS ingeladen na toestemming.
   - Google Analytics en Google Ads stel je in binnen Tag Manager.
   - Vul hieronder het container-ID in (GTM-XXXXXXX).
   ========================================================= */
(function () {
  var GTM_ID = 'GTM-XXXXXXX';          // <-- hier het Tag Manager-ID invullen
  var OPSLAG = 'stamgast_cookies';
  var VERSIE = 1;                      // verhoog bij wijziging van het cookiebeleid: iedereen krijgt de melding opnieuw
  var GELDIG_DAGEN = 180;              // na 6 maanden opnieuw vragen

  /* ---------- Consent Mode: standaard alles geweigerd ---------- */
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500
  });

  /* ---------- Opslag van de keuze ---------- */
  function leesKeuze() {
    try {
      var k = JSON.parse(localStorage.getItem(OPSLAG));
      if (!k || k.versie !== VERSIE) return null;
      if (Date.now() - k.datum > GELDIG_DAGEN * 864e5) return null;
      return k;
    } catch (e) { return null; }
  }
  function bewaarKeuze(statistieken, marketing) {
    var k = { statistieken: !!statistieken, marketing: !!marketing, datum: Date.now(), versie: VERSIE };
    try { localStorage.setItem(OPSLAG, JSON.stringify(k)); } catch (e) {}
    return k;
  }

  /* ---------- Toestemming toepassen ---------- */
  var gtmGeladen = false;
  function laadGTM() {
    if (gtmGeladen || !/^GTM-[A-Z0-9]+$/.test(GTM_ID) || GTM_ID === 'GTM-XXXXXXX') return;
    gtmGeladen = true;
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_ID;
    document.head.appendChild(s);
  }
  function verwijderGoogleCookies() {
    document.cookie.split(';').forEach(function (c) {
      var naam = c.split('=')[0].trim();
      if (/^(_ga|_gid|_gat|_gcl)/.test(naam)) {
        var host = location.hostname;
        var domeinen = ['', host, '.' + host, '.' + host.split('.').slice(-2).join('.')];
        domeinen.forEach(function (d) {
          document.cookie = naam + '=; Max-Age=0; path=/' + (d ? '; domain=' + d : '');
        });
      }
    });
  }
  function pasToe(k, wasAkkoord) {
    gtag('consent', 'update', {
      analytics_storage: k.statistieken ? 'granted' : 'denied',
      ad_storage: k.marketing ? 'granted' : 'denied',
      ad_user_data: k.marketing ? 'granted' : 'denied',
      ad_personalization: k.marketing ? 'granted' : 'denied'
    });
    if (k.statistieken || k.marketing) {
      laadGTM();
    } else if (wasAkkoord) {
      // toestemming ingetrokken: cookies opruimen en pagina herladen zodat Tag Manager niet meer actief is
      verwijderGoogleCookies();
      location.reload();
    }
  }

  /* ---------- Opmaak ---------- */
  var css = '' +
    '.ck-melding{position:fixed;left:16px;right:16px;bottom:16px;z-index:9999;max-width:560px;margin-left:auto;background:#fff;color:var(--tekst,#1c2420);border:1px solid var(--rand,#e2e6ea);border-radius:14px;box-shadow:0 10px 40px rgba(20,40,28,.18);padding:22px 22px 18px;font-family:inherit;}' +
    '.ck-melding h2{font-size:17px;font-weight:600;margin:0 0 6px;color:var(--primair,#233629);}' +
    '.ck-melding p{font-size:14px;line-height:1.6;color:var(--tekst-muted,#5a6672);margin:0 0 16px;}' +
    '.ck-melding a,.ck-paneel a{color:var(--groen,#2A5C3F);text-decoration:underline;text-underline-offset:2px;}' +
    '.ck-knoppen{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end;}' +
    '.ck-knop{font:inherit;font-size:14px;font-weight:500;border-radius:8px;padding:10px 16px;cursor:pointer;border:1px solid transparent;line-height:1.2;}' +
    '.ck-knop-grijs{background:#eef0ee;color:#4a5550;border-color:#e2e5e2;}' +
    '.ck-knop-grijs:hover{background:#e4e7e4;}' +
    '.ck-knop-kleur{background:var(--groen,#2A5C3F);color:#fff;font-weight:600;padding:10px 20px;}' +
    '.ck-knop-kleur:hover{filter:brightness(1.12);}' +
    '.ck-knop:focus-visible{outline:2px solid var(--oranje,#E85F2B);outline-offset:2px;}' +
    '.ck-achtergrond{position:fixed;inset:0;z-index:10000;background:rgba(20,30,24,.45);display:flex;align-items:center;justify-content:center;padding:16px;}' +
    '.ck-paneel{background:#fff;border-radius:14px;max-width:520px;width:100%;max-height:calc(100vh - 32px);overflow:auto;padding:24px;box-shadow:0 10px 40px rgba(0,0,0,.2);}' +
    '.ck-paneel h2{font-size:19px;font-weight:600;margin:0 0 6px;color:var(--primair,#233629);}' +
    '.ck-paneel > p{font-size:14px;line-height:1.6;color:var(--tekst-muted,#5a6672);margin:0 0 16px;}' +
    '.ck-cat{border-top:1px solid var(--rand,#e2e6ea);padding:14px 0;display:flex;gap:16px;align-items:flex-start;justify-content:space-between;}' +
    '.ck-cat strong{display:block;font-size:15px;margin-bottom:2px;}' +
    '.ck-cat span{font-size:13px;line-height:1.5;color:var(--tekst-muted,#5a6672);}' +
    '.ck-schakel{position:relative;flex:0 0 44px;width:44px;height:24px;margin-top:2px;}' +
    '.ck-schakel input{opacity:0;width:100%;height:100%;margin:0;position:absolute;inset:0;cursor:pointer;z-index:1;}' +
    '.ck-schakel i{position:absolute;inset:0;background:#cfd5d1;border-radius:24px;transition:background .2s;}' +
    '.ck-schakel i:before{content:"";position:absolute;width:18px;height:18px;left:3px;top:3px;background:#fff;border-radius:50%;transition:transform .2s;}' +
    '.ck-schakel input:checked + i{background:var(--groen,#2A5C3F);}' +
    '.ck-schakel input:checked + i:before{transform:translateX(20px);}' +
    '.ck-schakel input:disabled{cursor:not-allowed;}' +
    '.ck-schakel input:disabled + i{opacity:.55;}' +
    '.ck-schakel input:focus-visible + i{outline:2px solid var(--oranje,#E85F2B);outline-offset:2px;}' +
    '.ck-paneel .ck-knoppen{border-top:1px solid var(--rand,#e2e6ea);padding-top:16px;}' +
    '@media (max-width:520px){.ck-melding{left:12px;right:12px;bottom:12px;padding:18px 16px 14px;}.ck-knoppen{flex-direction:column-reverse;}.ck-knop{width:100%;padding:12px 16px;}}';

  function voegCssToe() {
    if (document.getElementById('ck-css')) return;
    var st = document.createElement('style');
    st.id = 'ck-css';
    st.textContent = css;
    document.head.appendChild(st);
  }

  /* ---------- Melding ---------- */
  var melding = null;
  function toonMelding() {
    voegCssToe();
    if (melding) return;
    melding = document.createElement('div');
    melding.className = 'ck-melding';
    melding.setAttribute('role', 'dialog');
    melding.setAttribute('aria-live', 'polite');
    melding.setAttribute('aria-label', 'Cookietoestemming');
    melding.innerHTML =
      '<h2>Mogen we cookies gebruiken?</h2>' +
      '<p>Met jouw toestemming gebruiken we cookies van Google om te zien hoe bezoekers de website gebruiken en om onze advertenties te meten. ' +
      'Meer info in ons <a href="cookiebeleid.html">cookiebeleid</a>.</p>' +
      '<div class="ck-knoppen">' +
      '<button type="button" class="ck-knop ck-knop-grijs" data-ck="aanpassen">Aanpassen</button>' +
      '<button type="button" class="ck-knop ck-knop-grijs" data-ck="weigeren">Weigeren</button>' +
      '<button type="button" class="ck-knop ck-knop-kleur" data-ck="alles">Accepteer alles</button>' +
      '</div>';
    melding.addEventListener('click', function (e) {
      var actie = e.target.getAttribute && e.target.getAttribute('data-ck');
      if (actie === 'alles') kies(true, true);
      if (actie === 'weigeren') kies(false, false);
      if (actie === 'aanpassen') toonPaneel();
    });
    document.body.appendChild(melding);
  }
  function verbergMelding() {
    if (melding) { melding.remove(); melding = null; }
  }

  /* ---------- Instellingenpaneel ---------- */
  function toonPaneel() {
    voegCssToe();
    var huidig = leesKeuze() || { statistieken: false, marketing: false };
    var achter = document.createElement('div');
    achter.className = 'ck-achtergrond';
    achter.innerHTML =
      '<div class="ck-paneel" role="dialog" aria-modal="true" aria-labelledby="ck-titel">' +
      '<h2 id="ck-titel">Cookie-instellingen</h2>' +
      '<p>Kies welke cookies je toestaat. Je kan je keuze altijd wijzigen via "Cookie-instellingen" onderaan elke pagina.</p>' +
      '<div class="ck-cat"><div><strong>Noodzakelijk</strong><span>Onthoudt je cookiekeuze. Altijd actief.</span></div>' +
      '<label class="ck-schakel"><input type="checkbox" checked disabled aria-label="Noodzakelijk, altijd actief"/><i></i></label></div>' +
      '<div class="ck-cat"><div><strong>Statistieken</strong><span>Google Analytics: inzicht in hoe bezoekers de website gebruiken.</span></div>' +
      '<label class="ck-schakel"><input type="checkbox" id="ck-stat" aria-label="Statistieken"' + (huidig.statistieken ? ' checked' : '') + '/><i></i></label></div>' +
      '<div class="ck-cat"><div><strong>Marketing</strong><span>Google Ads: meten welke advertenties tot een aanvraag leiden.</span></div>' +
      '<label class="ck-schakel"><input type="checkbox" id="ck-mark" aria-label="Marketing"' + (huidig.marketing ? ' checked' : '') + '/><i></i></label></div>' +
      '<div class="ck-knoppen">' +
      '<button type="button" class="ck-knop ck-knop-grijs" data-ck="opslaan">Keuze opslaan</button>' +
      '<button type="button" class="ck-knop ck-knop-kleur" data-ck="alles">Accepteer alles</button>' +
      '</div></div>';
    function sluit() { achter.remove(); document.removeEventListener('keydown', esc); }
    function esc(e) { if (e.key === 'Escape') sluit(); }
    achter.addEventListener('click', function (e) {
      if (e.target === achter) { sluit(); return; }
      var actie = e.target.getAttribute && e.target.getAttribute('data-ck');
      if (actie === 'alles') { kies(true, true); sluit(); }
      if (actie === 'opslaan') {
        kies(achter.querySelector('#ck-stat').checked, achter.querySelector('#ck-mark').checked);
        sluit();
      }
    });
    document.addEventListener('keydown', esc);
    document.body.appendChild(achter);
    var eerste = achter.querySelector('#ck-stat');
    if (eerste) eerste.focus();
  }

  function kies(statistieken, marketing) {
    var vorige = leesKeuze();
    var wasAkkoord = !!(vorige && (vorige.statistieken || vorige.marketing));
    var k = bewaarKeuze(statistieken, marketing);
    verbergMelding();
    pasToe(k, wasAkkoord && !(statistieken || marketing));
  }

  /* ---------- Start ---------- */
  var keuze = leesKeuze();
  if (keuze) pasToe(keuze, false);

  function start() {
    if (!leesKeuze()) toonMelding();
    document.addEventListener('click', function (e) {
      var link = e.target.closest && e.target.closest('[data-cookie-instellingen]');
      if (link) { e.preventDefault(); toonPaneel(); }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
