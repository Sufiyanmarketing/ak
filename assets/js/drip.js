/*
 * Drip – sporing og hendelser
 *
 * Sett DRIP_ACCOUNT_ID til konto-ID-en din (tallet i Drip-URL-en:
 * https://www.getdrip.com/<KONTO-ID>/...). Så lenge den står tom,
 * lastes ikke Drip i det hele tatt.
 *
 * NB: Bruk aldri API-tokenet ditt her. Alt i denne filen er offentlig
 * synlig for alle som besøker siden. Konto-ID-en er trygg å eksponere.
 */
(function () {
  var DRIP_ACCOUNT_ID = ''; // f.eks. '1234567'

  if (!/^\d+$/.test(DRIP_ACCOUNT_ID)) return;

  window._dcq = window._dcq || [];
  window._dcs = window._dcs || {};
  window._dcs.account = DRIP_ACCOUNT_ID;

  var dc = document.createElement('script');
  dc.async = true;
  dc.src = 'https://tag.getdrip.com/' + DRIP_ACCOUNT_ID + '.js';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(dc, s);

  // Hendelse når noen klikker på en påmeldingsknapp (vises på kjente abonnenter i Drip)
  document.addEventListener('click', function (e) {
    var link = e.target.closest && e.target.closest('a[href*="/checkout"]');
    if (!link) return;
    var section = link.closest('section, header, [data-sticky-cta]');
    window._dcq.push(['track', 'Klikket Meld deg på', {
      program: 'Kunsten å overbevise',
      plassering: (section && (section.id || section.className.split(' ')[0])) || 'ukjent'
    }]);
  });
})();
