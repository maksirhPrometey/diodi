(function () {
  'use strict';

  function qs(selector, root) {
    return (root || document).querySelector(selector);
  }

  function qsa(selector, root) {
    return Array.from((root || document).querySelectorAll(selector));
  }

  window.diodi = window.diodi || {};
  window.diodi.qs = qs;
  window.diodi.qsa = qsa;
})();
