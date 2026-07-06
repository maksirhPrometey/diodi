(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    var scrollBtn = document.querySelector('[data-scroll-top]');
    if (scrollBtn) {
      window.addEventListener('scroll', function () {
        scrollBtn.classList.toggle('is-visible', window.scrollY > 420);
      }, { passive: true });
      scrollBtn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    }

    document.body.addEventListener('click', function (event) {
      var trigger = event.target.closest('[data-lightbox]');
      if (!trigger) {
        return;
      }
      var label = trigger.getAttribute('data-lightbox') || '';
      var imageUrl = trigger.getAttribute('data-image-url') || '';
      var bgClass = 'bg-gradient-0';
      trigger.classList.forEach(function (cls) {
        if (cls.indexOf('bg-gradient-') === 0) {
          bgClass = cls;
        }
      });

      var contentHtml;
      if (imageUrl) {
        contentHtml =
          '<img class="lightbox__photo" src="' + imageUrl + '" alt="' + label + '">' +
          '<span class="media-placeholder__caption">' + label + '</span>';
      } else {
        contentHtml =
          '<span class="lightbox__image-icon">' +
          '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">' +
          '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M3 17l5-4 4 3 3-3 6 5"/>' +
          '</svg></span>' +
          '<span class="media-placeholder__caption">' + label + '</span>';
      }

      var overlay = document.createElement('div');
      overlay.className = 'lightbox';
      overlay.innerHTML =
        '<button type="button" class="lightbox__close" aria-label="Закрити">' +
        '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>' +
        '</button>' +
        '<div class="lightbox__content ' + (imageUrl ? 'lightbox__content--photo' : bgClass) + '">' +
        contentHtml +
        '</div>';

      overlay.addEventListener('click', function (e) {
        if (e.target === overlay || e.target.closest('.lightbox__close')) {
          overlay.remove();
        }
      });
      overlay.querySelector('.lightbox__content').addEventListener('click', function (e) {
        e.stopPropagation();
      });
      document.body.appendChild(overlay);
    });
  });
})();
