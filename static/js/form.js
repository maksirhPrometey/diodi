(function () {
  'use strict';

  document.addEventListener('htmx:beforeSwap', function (event) {
    if (event.detail.xhr.status === 422) {
      event.detail.shouldSwap = true;
      event.detail.isError = false;
    }
  });

  document.addEventListener('htmx:beforeRequest', function (event) {
    var submit = event.detail.elt.querySelector('.form-submit');
    if (submit) {
      submit.classList.add('is-loading');
      submit.textContent = 'Надсилання…';
    }
  });

  document.addEventListener('htmx:afterRequest', function (event) {
    var submit = event.detail.elt.querySelector('.form-submit');
    if (submit && event.detail.failed) {
      submit.classList.remove('is-loading');
      submit.textContent = 'ВІДПРАВИТИ';
    }
  });
})();
