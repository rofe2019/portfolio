/* Portfolio interactions: nav, reveal, filters, lightbox, spotlight cards */
(function () {
	'use strict';

	var body = document.body;
	var nav = document.querySelector('.site-nav');
	var toggle = document.querySelector('.nav-toggle');
	var toTop = document.querySelector('.to-top');

	/* Sticky nav state + back-to-top */
	function onScroll() {
		var y = window.scrollY || window.pageYOffset;
		if (nav) nav.classList.toggle('scrolled', y > 24);
		if (toTop) toTop.classList.toggle('show', y > 600);
	}
	window.addEventListener('scroll', onScroll, { passive: true });
	onScroll();

	/* Mobile menu */
	if (toggle) {
		toggle.addEventListener('click', function () {
			body.classList.toggle('menu-open');
			toggle.setAttribute('aria-expanded', body.classList.contains('menu-open'));
		});
		document.querySelectorAll('.nav-links a').forEach(function (a) {
			a.addEventListener('click', function () { body.classList.remove('menu-open'); });
		});
		document.addEventListener('keydown', function (e) {
			if (e.key === 'Escape') body.classList.remove('menu-open');
		});
	}

	/* Active nav link while scrolling (home page only) */
	var sections = Array.prototype.slice.call(document.querySelectorAll('section[id]'));
	var links = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
	if (sections.length && links.length && 'IntersectionObserver' in window) {
		var spy = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (!entry.isIntersecting) return;
				links.forEach(function (l) {
					l.classList.toggle('active', l.getAttribute('href') === '#' + entry.target.id);
				});
			});
		}, { rootMargin: '-40% 0px -55% 0px' });
		sections.forEach(function (s) { spy.observe(s); });
	}

	/* Scroll reveal */
	var reveals = document.querySelectorAll('.reveal');
	if ('IntersectionObserver' in window) {
		var io = new IntersectionObserver(function (entries) {
			entries.forEach(function (entry) {
				if (entry.isIntersecting) {
					entry.target.classList.add('in');
					io.unobserve(entry.target);
				}
			});
		}, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
		reveals.forEach(function (el) { io.observe(el); });
	} else {
		reveals.forEach(function (el) { el.classList.add('in'); });
	}

	/* Spotlight hover on cards */
	document.querySelectorAll('.card').forEach(function (card) {
		card.addEventListener('pointermove', function (e) {
			var r = card.getBoundingClientRect();
			card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
			card.style.setProperty('--my', (e.clientY - r.top) + 'px');
		});
	});

	/* Project filters */
	var filterBtns = document.querySelectorAll('.filter-btn');
	var cards = document.querySelectorAll('.project-card');
	filterBtns.forEach(function (btn) {
		btn.addEventListener('click', function () {
			var f = btn.getAttribute('data-filter');
			filterBtns.forEach(function (b) { b.classList.toggle('active', b === btn); });
			var i = 0;
			cards.forEach(function (card) {
				var match = f === 'all' || (card.getAttribute('data-cat') || '').split(' ').indexOf(f) !== -1;
				card.classList.toggle('hidden', !match);
				if (match) {
					card.classList.remove('in');
					card.style.setProperty('--d', (i++ % 9) * 0.05 + 's');
					requestAnimationFrame(function () { requestAnimationFrame(function () { card.classList.add('in'); }); });
				}
			});
		});
	});

	/* Lightbox */
	var shots = Array.prototype.slice.call(document.querySelectorAll('.shot'));
	if (shots.length) {
		var lb = document.createElement('div');
		lb.className = 'lightbox';
		lb.setAttribute('role', 'dialog');
		lb.setAttribute('aria-label', 'Screenshot viewer');
		lb.innerHTML =
			'<button class="lb-close" aria-label="Close"><i class="fas fa-times"></i></button>' +
			'<button class="lb-prev" aria-label="Previous"><i class="fas fa-chevron-left"></i></button>' +
			'<img alt="" />' +
			'<button class="lb-next" aria-label="Next"><i class="fas fa-chevron-right"></i></button>' +
			'<div class="lb-count"></div>';
		document.body.appendChild(lb);

		var img = lb.querySelector('img');
		var count = lb.querySelector('.lb-count');
		var current = 0;

		function show(i) {
			current = (i + shots.length) % shots.length;
			var src = shots[current].getAttribute('href') || shots[current].querySelector('img').src;
			img.src = src;
			img.alt = shots[current].querySelector('img').alt || '';
			count.textContent = (current + 1) + ' / ' + shots.length;
		}
		function open(i) { show(i); lb.classList.add('open'); body.style.overflow = 'hidden'; }
		function close() { lb.classList.remove('open'); body.style.overflow = ''; }

		shots.forEach(function (s, i) {
			s.addEventListener('click', function (e) { e.preventDefault(); open(i); });
		});
		lb.querySelector('.lb-close').addEventListener('click', close);
		lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(current - 1); });
		lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(current + 1); });
		lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
		document.addEventListener('keydown', function (e) {
			if (!lb.classList.contains('open')) return;
			if (e.key === 'Escape') close();
			if (e.key === 'ArrowLeft') show(current - 1);
			if (e.key === 'ArrowRight') show(current + 1);
		});

		var touchX = null;
		lb.addEventListener('touchstart', function (e) { touchX = e.touches[0].clientX; }, { passive: true });
		lb.addEventListener('touchend', function (e) {
			if (touchX === null) return;
			var dx = e.changedTouches[0].clientX - touchX;
			if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
			touchX = null;
		});
	}

	/* Footer year */
	document.querySelectorAll('[data-year]').forEach(function (el) {
		el.textContent = new Date().getFullYear();
	});
})();
