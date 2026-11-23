/**
 * Birthday Surprise Engine - Phase 2 Romantic Edition
 * محرك موقع مفاجأة عيد ميلاد رفوووووق — جواب حب وورد، ظرف ٢٣ نوفمبر، وألبوم الذكريات
 */

(function () {
  'use strict';

  // التحقق من وجود ملف الإعدادات
  const config = typeof BIRTHDAY_CONFIG !== 'undefined' ? BIRTHDAY_CONFIG : {
    targetDateCairo: "2026-12-02T00:00:00+02:00",
    title: "يا رفووووووق ❤️",
    subtitle: "فاضل شوية على عيد ميلادك… وقبل ما ييجي، عايز أرجع معاكي ليوم بحبه أوي",
    photoDateBadge: "٢٣ نوفمبر",
    photoMemoryCaption: "فاكرة يوم ما أبونا صلّى على الدبل، وبعدها نزلنا أول ديت؟ كل ما ببص للصورة دي ببتسم",
    birthdayCelebrationTitle: "كل سنة وإنتِ طيبة يا رفووووووق ❤️",
    birthdayCelebrationSubtitle: "يا رب كل سنة وإحنا سوا وفي حضن بعض، ودايمًا منورة حياتي ومفرّحة قلبي 💍✨",
    heroImage: "assets/images/hero-selfie-rings.jpg",
    envelope: {
      name: "ظرف ٢٣ نوفمبر",
      envelopeLabel: "لرفووووووق",
      buttonText: "افتحي الجواب يا رفووووووق",
      subtitle: "ألبوم ذكريات يوم صلاة الدبل وأول ديت سوا",
      letterDedication: "يا رفووووووق، لو هختار يوم أعيشه معاكي تاني، يوم ٢٣ نوفمبر هييجي في بالي على طول. ❤️",
      closingMessage: "يوم ٢٣ نوفمبر كان حلو أوي عشان كنت معاكي… وكل سنة وإنتِ حبيبتي يا رفووووووق ❤️",
      signature: "بحبك"
    },
    albumPhotos: [
      { id: 1, title: "الصورة الجماعية مع أبونا", caption: "يوم ما أبونا صلّى على الدبل", src: "assets/images/photo-4-group-father.jpg", isGroupPhoto: true },
      { id: 2, title: "صورة المراية", caption: "أنا وإنتِ يوم ٢٣ نوفمبر", src: "assets/images/photo-1-mirror.jpg", isGroupPhoto: false },
      { id: 3, title: "السيلفي اللي في الافتتاح", caption: "وبعدها نزلنا أول ديت", src: "assets/images/hero-selfie-rings.jpg", isGroupPhoto: false },
      { id: 4, title: "السيلفي التانية بالدبل", caption: "كل ما أبص للصور دي ببتسم. بحبك يا رفووووووق ❤️", src: "assets/images/photo-3-selfie-rings-2.jpg", isGroupPhoto: false }
    ],
    timerLabels: { days: "يوم", hours: "ساعة", minutes: "دقيقة", seconds: "ثانية" }
  };

  // عناصر واجهة المستخدم
  const elements = {
    pageTitle: document.getElementById('pageTitle'),
    pageSubtitle: document.getElementById('pageSubtitle'),
    heroImage: document.getElementById('heroImage'),
    photoDateBadge: document.getElementById('photoDateBadge'),
    photoMemoryCaption: document.getElementById('photoMemoryCaption'),
    
    countdownSection: document.getElementById('countdownSection'),
    timerGrid: document.getElementById('timerGrid'),
    celebrationSection: document.getElementById('celebrationSection'),
    celebrationTitle: document.getElementById('celebrationTitle'),
    celebrationSubtitle: document.getElementById('celebrationSubtitle'),
    
    daysVal: document.getElementById('daysVal'),
    hoursVal: document.getElementById('hoursVal'),
    minutesVal: document.getElementById('minutesVal'),
    secondsVal: document.getElementById('secondsVal'),

    daysLabel: document.getElementById('daysLabel'),
    hoursLabel: document.getElementById('hoursLabel'),
    minutesLabel: document.getElementById('minutesLabel'),
    secondsLabel: document.getElementById('secondsLabel'),

    // مكوّنات ظرف وجواب ٢٣ نوفمبر
    envelopeContainer: document.getElementById('envelopeContainer'),
    envelopeOuter: document.getElementById('envelopeOuter'),
    envelopeFlap: document.getElementById('envelopeFlap'),
    envelopeSeal: document.getElementById('envelopeSeal'),
    openEnvelopeBtn: document.getElementById('openEnvelopeBtn'),
    petalsContainer: document.getElementById('petalsContainer'),

    // مكوّنات ألبوم جواب الحب
    memoryAlbumOverlay: document.getElementById('memoryAlbumOverlay'),
    albumBackdrop: document.getElementById('albumBackdrop'),
    loveLetterCard: document.getElementById('loveLetterCard'),
    closeAlbumBtn: document.getElementById('closeAlbumBtn'),
    letterDedicationQuote: document.getElementById('letterDedicationQuote'),
    albumPhotoViewport: document.getElementById('albumPhotoViewport'),
    albumCurrentImg: document.getElementById('albumCurrentImg'),
    albumCurrentCaption: document.getElementById('albumCurrentCaption'),
    currentPhotoNum: document.getElementById('currentPhotoNum'),
    totalPhotosNum: document.getElementById('totalPhotosNum'),
    albumPrevBtn: document.getElementById('albumPrevBtn'),
    albumNextBtn: document.getElementById('albumNextBtn'),
    albumDotsContainer: document.getElementById('albumDotsContainer'),
    albumPhotoFrame: document.getElementById('albumPhotoFrame'),
    albumClosingMsg: document.getElementById('albumClosingMsg'),

    sparklesCanvas: document.getElementById('sparklesCanvas'),

    // أدوات الاختبار
    devTestPanel: document.getElementById('devTestPanel'),
    devToggleBtn: document.getElementById('devToggleBtn'),
    btnTestNormal: document.getElementById('btnTestNormal'),
    btnTest3Sec: document.getElementById('btnTest3Sec'),
    btnTestZero: document.getElementById('btnTestZero'),
    btnTestAlbumDirect: document.getElementById('btnTestAlbumDirect'),
    devStatusText: document.getElementById('devStatusText')
  };

  // حالة النظام
  let timerInterval = null;
  let simulatedTargetTime = null;
  let isCelebrationActive = false;
  let currentAlbumIndex = 0;
  let hasTransitionedFromCountdown = false;
  let hasLaunchedPetals = false;
  let isOpeningEnvelope = false;

  /**
   * فحص بيئة التشغيل: هل هي بيئة محلية للمطور؟
   */
  function isLocalEnvironment() {
    const proto = window.location.protocol;
    const host = window.location.hostname;
    return proto === 'file:' || host === 'localhost' || host === '127.0.0.1' || host === '::1';
  }

  /**
   * فحص هل وضع الزائرة مفعل عبر المعامل (?mode=visitor)
   */
  function isVisitorMode() {
    const params = new URLSearchParams(window.location.search);
    return params.get('mode') === 'visitor' || params.get('visitor') === '1' || !isLocalEnvironment();
  }

  /**
   * تطبيق النصوص والإعدادات على عناصر DOM
   */
  function applyConfiguration() {
    if (elements.pageSubtitle && config.subtitle) {
      elements.pageSubtitle.textContent = config.subtitle;
    }
    if (elements.heroImage && config.heroImage) {
      elements.heroImage.src = config.heroImage;
    }
    if (elements.photoDateBadge && config.photoDateBadge) {
      const textSpan = elements.photoDateBadge.querySelector('.badge-text');
      if (textSpan) textSpan.textContent = config.photoDateBadge;
    }
    if (elements.photoMemoryCaption && config.photoMemoryCaption) {
      elements.photoMemoryCaption.textContent = config.photoMemoryCaption;
    }
    if (elements.celebrationTitle && config.birthdayCelebrationTitle) {
      elements.celebrationTitle.textContent = config.birthdayCelebrationTitle;
    }
    if (elements.celebrationSubtitle && config.birthdayCelebrationSubtitle) {
      elements.celebrationSubtitle.textContent = config.birthdayCelebrationSubtitle;
    }
    if (elements.openEnvelopeBtn && config.envelope && config.envelope.buttonText) {
      const btnText = elements.openEnvelopeBtn.querySelector('.btn-text');
      if (btnText) btnText.textContent = config.envelope.buttonText;
    }
    if (elements.letterDedicationQuote && config.envelope && config.envelope.letterDedication) {
      elements.letterDedicationQuote.textContent = `«${config.envelope.letterDedication.replace(/^[«»\s]+|[«»\s]+$/g, '')}»`;
    }
    if (elements.albumClosingMsg && config.envelope && config.envelope.closingMessage) {
      elements.albumClosingMsg.textContent = `«${config.envelope.closingMessage.replace(/^[«»\s]+|[«»\s]+$/g, '')}»`;
    }
    if (config.timerLabels) {
      if (elements.daysLabel) elements.daysLabel.textContent = config.timerLabels.days || "يوم";
      if (elements.hoursLabel) elements.hoursLabel.textContent = config.timerLabels.hours || "ساعة";
      if (elements.minutesLabel) elements.minutesLabel.textContent = config.timerLabels.minutes || "دقيقة";
      if (elements.secondsLabel) elements.secondsLabel.textContent = config.timerLabels.seconds || "ثانية";
    }

    initAlbumDots();
  }

  /**
   * حساب الوقت المتبقي بالنسبة لتوقيت القاهرة الثابت (+02:00)
   */
  function getRemainingTime() {
    let targetMs;
    if (simulatedTargetTime !== null) {
      targetMs = simulatedTargetTime;
    } else {
      targetMs = new Date(config.targetDateCairo).getTime();
    }

    const nowMs = Date.now();
    const diffMs = targetMs - nowMs;

    if (diffMs <= 0) {
      return { total: 0, days: 0, hours: 0, minutes: 0, seconds: 0, isZero: true };
    }

    const totalSeconds = Math.floor(diffMs / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    return { total: diffMs, days, hours, minutes, seconds, isZero: false };
  }

  function formatNumber(num) {
    return String(num).padStart(2, '0');
  }

  /**
   * تحديث واجهة العدّاد وضبط لحظة الصفر السلسة
   */
  function updateCountdownDisplay() {
    const time = getRemainingTime();

    if (time.isZero) {
      // عرض الأصفار أولاً للتطابق مع لحظة الوصول للصفر
      if (elements.daysVal) elements.daysVal.textContent = "00";
      if (elements.hoursVal) elements.hoursVal.textContent = "00";
      if (elements.minutesVal) elements.minutesVal.textContent = "00";
      if (elements.secondsVal) elements.secondsVal.textContent = "00";

      if (elements.timerGrid) {
        elements.timerGrid.classList.add('zero-pulse');
      }

      // إذا كانت الصفحة مفتوحة أثناء العدّاد، ننتظر 450ms ليرى الزائر الصفر ثم يفتح الاحتفال
      if (hasTransitionedFromCountdown) {
        setTimeout(() => {
          triggerCelebration(true);
        }, 450);
      } else {
        triggerCelebration(false);
      }
      return;
    }

    hasTransitionedFromCountdown = true;

    if (elements.daysVal) elements.daysVal.textContent = formatNumber(time.days);
    if (elements.hoursVal) elements.hoursVal.textContent = formatNumber(time.hours);
    if (elements.minutesVal) elements.minutesVal.textContent = formatNumber(time.minutes);
    if (elements.secondsVal) elements.secondsVal.textContent = formatNumber(time.seconds);
  }

  /**
   * تفعيل حالة الاحتفال عند الصفر
   */
  function triggerCelebration(animate = false) {
    if (isCelebrationActive) return;
    isCelebrationActive = true;

    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }

    if (elements.countdownSection) {
      if (animate) {
        elements.countdownSection.style.opacity = '0';
        elements.countdownSection.style.transform = 'translateY(-10px)';
        setTimeout(() => {
          elements.countdownSection.style.display = 'none';
        }, 350);
      } else {
        elements.countdownSection.style.display = 'none';
      }
    }

    if (elements.celebrationSection) {
      elements.celebrationSection.classList.remove('hidden');
      if (animate) {
        setTimeout(() => {
          elements.celebrationSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 300);
      }
    }

    launchCelebrationParticles();
  }

  /**
   * إعادة ضبط العرض لحالة العد التنازلي النشط
   */
  function resetToCountdown() {
    isCelebrationActive = false;
    hasTransitionedFromCountdown = false;
    isOpeningEnvelope = false;

    if (elements.timerGrid) {
      elements.timerGrid.classList.remove('zero-pulse');
    }

    if (elements.countdownSection) {
      elements.countdownSection.style.display = 'block';
      setTimeout(() => {
        elements.countdownSection.style.opacity = '1';
        elements.countdownSection.style.transform = 'translateY(0)';
      }, 50);
    }

    if (elements.celebrationSection) {
      elements.celebrationSection.classList.add('hidden');
    }

    if (elements.envelopeOuter) {
      elements.envelopeOuter.classList.remove('is-open', 'is-breaking-seal');
    }

    if (elements.memoryAlbumOverlay) {
      elements.memoryAlbumOverlay.classList.add('hidden');
    }

    if (timerInterval) {
      clearInterval(timerInterval);
    }

    updateCountdownDisplay();
    timerInterval = setInterval(updateCountdownDisplay, 1000);
  }

  /**
   * حركة متسلسلة واحدة لفتح الجواب وظرف ٢٣ نوفمبر
   */
  function setupEnvelopeEvents() {
    function executeOpenSequence() {
      if (isOpeningEnvelope) return;
      isOpeningEnvelope = true;

      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      // إذا كان تقليل الحركة مفعلاً، يتم فتح الجواب والألبوم فوراً
      if (prefersReduced) {
        if (elements.envelopeOuter) {
          elements.envelopeOuter.classList.add('is-open');
        }
        openAlbumModal(0);
        isOpeningEnvelope = false;
        return;
      }

      // الحركة المتسلسلة:
      // ١. تفكيك الختم الوردي الغامق
      if (elements.envelopeOuter) {
        elements.envelopeOuter.classList.add('is-breaking-seal');
      }

      // ٢. فتح غطاء الظرف
      setTimeout(() => {
        if (elements.envelopeOuter) {
          elements.envelopeOuter.classList.add('is-open');
        }
      }, 200);

      // ٣. إطلاق بتلات الورد المتطايرة على الجانبين (مرة واحدة فقط)
      setTimeout(() => {
        launchRosePetals();
      }, 350);

      // ٤. انبثاق الجواب وظهور الألبوم
      setTimeout(() => {
        openAlbumModal(0);
        isOpeningEnvelope = false;
      }, 650);
    }

    if (elements.openEnvelopeBtn) {
      elements.openEnvelopeBtn.addEventListener('click', executeOpenSequence);
    }
    if (elements.envelopeOuter) {
      elements.envelopeOuter.addEventListener('click', executeOpenSequence);
    }
  }

  /**
   * إطلاق بتلات الورد على جانبي الشاشة (مرة واحدة عند فتح الظرف)
   */
  function launchRosePetals() {
    if (hasLaunchedPetals || !elements.petalsContainer) return;
    hasLaunchedPetals = true;

    const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) return;

    elements.petalsContainer.innerHTML = '';
    const petalCount = 24;

    for (let i = 0; i < petalCount; i++) {
      const petal = document.createElement('div');
      petal.className = 'rose-petal';
      
      // التوزيع على الجانبين الأيمن والأيسر بعيداً عن منتصف المحتوى
      const isLeft = i % 2 === 0;
      const leftPercent = isLeft 
        ? Math.random() * 20 + 2  // بين 2% و 22% على اليسار
        : Math.random() * 20 + 78; // بين 78% و 98% على اليمين

      const size = Math.random() * 12 + 12; // بين 12px و 24px
      const delay = Math.random() * 0.8;
      const duration = Math.random() * 1.5 + 2.5;

      petal.style.left = `${leftPercent}%`;
      petal.style.width = `${size}px`;
      petal.style.height = `${size * 1.25}px`;
      petal.style.animationDelay = `${delay}s`;
      petal.style.animationDuration = `${duration}s`;

      elements.petalsContainer.appendChild(petal);
    }

    // تنظيف البتلات بعد انتهاء الحركة
    setTimeout(() => {
      if (elements.petalsContainer) {
        elements.petalsContainer.innerHTML = '';
      }
    }, 4500);
  }

  /**
   * إعداد دوائر مؤشرات ألبوم الصور
   */
  function initAlbumDots() {
    if (!elements.albumDotsContainer) return;
    elements.albumDotsContainer.innerHTML = '';
    const photos = config.albumPhotos || [];

    if (elements.totalPhotosNum) {
      elements.totalPhotosNum.textContent = String(photos.length);
    }

    photos.forEach((photo, idx) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = `album-dot ${idx === 0 ? 'active' : ''}`;
      dot.setAttribute('aria-label', `الانتقال إلى صورة ${idx + 1}`);
      dot.addEventListener('click', () => {
        showAlbumPhoto(idx);
      });
      elements.albumDotsContainer.appendChild(dot);
    });
  }

  /**
   * فتح نافذة ألبوم الذكريات وجواب الحب
   */
  function openAlbumModal(index = 0) {
    if (!elements.memoryAlbumOverlay) return;
    elements.memoryAlbumOverlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    showAlbumPhoto(index);
  }

  /**
   * إغلاق نافذة الألبوم
   */
  function closeAlbumModal() {
    if (!elements.memoryAlbumOverlay) return;
    elements.memoryAlbumOverlay.classList.add('hidden');
    document.body.style.overflow = '';
  }

  /**
   * عرض صورة محددة في الألبوم وتحديث التنسيق والنصوص
   */
  function showAlbumPhoto(index) {
    const photos = config.albumPhotos || [];
    if (!photos.length) return;

    if (index < 0) index = 0;
    if (index >= photos.length) index = photos.length - 1;

    currentAlbumIndex = index;
    const photo = photos[index];

    // تحديث رقم الصورة الحالية
    if (elements.currentPhotoNum) {
      elements.currentPhotoNum.textContent = String(index + 1);
    }

    // تطبيق الصورة والنص
    if (elements.albumCurrentImg) {
      elements.albumCurrentImg.src = photo.src;
      elements.albumCurrentImg.alt = photo.title || photo.caption;
    }

    if (elements.albumCurrentCaption) {
      elements.albumCurrentCaption.textContent = photo.caption;
    }

    // تخصيص عرض الصورة الجماعية لظهور كل الأشخاص
    if (elements.albumPhotoViewport) {
      if (photo.isGroupPhoto) {
        elements.albumPhotoViewport.classList.add('is-group-photo');
      } else {
        elements.albumPhotoViewport.classList.remove('is-group-photo');
      }
    }

    // تحديث حالة أزرار التنقل (السابق / التالي)
    if (elements.albumPrevBtn) {
      elements.albumPrevBtn.disabled = (index === 0);
    }
    if (elements.albumNextBtn) {
      elements.albumNextBtn.disabled = (index === photos.length - 1);
    }

    // تحديث الدوائر
    if (elements.albumDotsContainer) {
      const dots = elements.albumDotsContainer.querySelectorAll('.album-dot');
      dots.forEach((dot, dIdx) => {
        if (dIdx === index) {
          dot.classList.add('active');
        } else {
          dot.classList.remove('active');
        }
      });
    }
  }

  /**
   * إعداد أحداث ألبوم الذكريات (كيبورد، لمس، أزرار)
   */
  function setupAlbumEvents() {
    if (elements.closeAlbumBtn) {
      elements.closeAlbumBtn.addEventListener('click', closeAlbumModal);
    }
    if (elements.albumBackdrop) {
      elements.albumBackdrop.addEventListener('click', closeAlbumModal);
    }

    // أزرار السابق والتالي (في RTL: السابق يعود للوراء، والتالي يتقدم للأمام)
    if (elements.albumPrevBtn) {
      elements.albumPrevBtn.addEventListener('click', () => {
        if (currentAlbumIndex > 0) {
          showAlbumPhoto(currentAlbumIndex - 1);
        }
      });
    }
    if (elements.albumNextBtn) {
      elements.albumNextBtn.addEventListener('click', () => {
        const photos = config.albumPhotos || [];
        if (currentAlbumIndex < photos.length - 1) {
          showAlbumPhoto(currentAlbumIndex + 1);
        }
      });
    }

    // دعم لوحة المفاتيح
    document.addEventListener('keydown', (e) => {
      if (!elements.memoryAlbumOverlay || elements.memoryAlbumOverlay.classList.contains('hidden')) {
        return;
      }
      if (e.key === 'Escape') {
        closeAlbumModal();
      } else if (e.key === 'ArrowLeft') {
        // في RTL، السهم لليسار هو الاتجاه للأمام (التالي)
        const photos = config.albumPhotos || [];
        if (currentAlbumIndex < photos.length - 1) {
          showAlbumPhoto(currentAlbumIndex + 1);
        }
      } else if (e.key === 'ArrowRight') {
        // في RTL، السهم لليمين هو الاتجاه للوراء (السابق)
        if (currentAlbumIndex > 0) {
          showAlbumPhoto(currentAlbumIndex - 1);
        }
      }
    });

    // دعم السحب باللمس على شاشات الموبايل (Touch Swipe)
    let touchStartX = 0;
    let touchEndX = 0;

    if (elements.albumPhotoFrame) {
      elements.albumPhotoFrame.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      elements.albumPhotoFrame.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipeGesture();
      }, { passive: true });
    }

    function handleSwipeGesture() {
      const swipeDistance = touchEndX - touchStartX;
      const minSwipe = 40;

      if (Math.abs(swipeDistance) < minSwipe) return;

      const photos = config.albumPhotos || [];
      if (swipeDistance < 0) {
        // سحب لليسار -> التالي
        if (currentAlbumIndex < photos.length - 1) {
          showAlbumPhoto(currentAlbumIndex + 1);
        }
      } else {
        // سحب لليمين -> السابق
        if (currentAlbumIndex > 0) {
          showAlbumPhoto(currentAlbumIndex - 1);
        }
      }
    }
  }

  /**
   * محرك النجوم المتلألئة وتأثير الاحتفال (Canvas)
   */
  let canvas = null;
  let ctx = null;
  let particles = [];
  let animationFrameId = null;

  function initSparklesCanvas() {
    canvas = elements.sparklesCanvas;
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    particles = [];
    const count = window.innerWidth < 600 ? 30 : 55;
    for (let i = 0; i < count; i++) {
      particles.push(createAmbientStar());
    }

    renderParticles();
  }

  function createAmbientStar() {
    return {
      type: 'ambient',
      x: Math.random() * (canvas ? canvas.width : window.innerWidth),
      y: Math.random() * (canvas ? canvas.height : window.innerHeight),
      size: Math.random() * 1.8 + 0.6,
      opacity: Math.random() * 0.7 + 0.2,
      speedX: (Math.random() - 0.5) * 0.25,
      speedY: -Math.random() * 0.35 - 0.05,
      pulseSpeed: Math.random() * 0.02 + 0.008,
      color: Math.random() > 0.4 ? '229, 195, 120' : '255, 255, 255'
    };
  }

  function launchCelebrationParticles() {
    if (!canvas || !ctx) return;
    for (let i = 0; i < 75; i++) {
      particles.push({
        type: Math.random() > 0.5 ? 'heart' : 'confetti',
        x: canvas.width * 0.5 + (Math.random() - 0.5) * 200,
        y: canvas.height * 0.35 + (Math.random() - 0.5) * 100,
        size: Math.random() * 8 + 6,
        vx: (Math.random() - 0.5) * 8,
        vy: -Math.random() * 9 - 4,
        gravity: 0.18,
        rotation: Math.random() * 360,
        rotationSpeed: (Math.random() - 0.5) * 8,
        opacity: 1,
        fadeSpeed: Math.random() * 0.008 + 0.003,
        color: ['#ba1e36', '#e5c378', '#ffd880', '#e85973', '#ffffff', '#ff9eb1'][Math.floor(Math.random() * 6)]
      });
    }
  }

  function renderParticles() {
    if (!ctx || !canvas) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];

      if (p.type === 'ambient') {
        p.y += p.speedY;
        p.x += p.speedX;
        p.opacity += Math.sin(Date.now() * p.pulseSpeed) * 0.01;

        if (p.y < 0) p.y = canvas.height;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;

        ctx.fillStyle = `rgba(${p.color}, ${Math.max(0.1, Math.min(0.9, p.opacity))})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      } else if (p.type === 'heart') {
        p.vy += p.gravity;
        p.x += p.vx;
        p.y += p.vy;
        p.opacity -= p.fadeSpeed;
        p.rotation += p.rotationSpeed;

        if (p.opacity > 0) {
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = p.opacity;
          ctx.fillStyle = p.color;
          ctx.beginPath();
          const s = p.size * 0.6;
          ctx.moveTo(0, 0);
          ctx.bezierCurveTo(-s, -s, -s * 1.5, s * 0.4, 0, s * 1.4);
          ctx.bezierCurveTo(s * 1.5, s * 0.4, s, -s, 0, 0);
          ctx.fill();
          ctx.restore();
        } else {
          particles.splice(i, 1);
        }
      } else if (p.type === 'confetti') {
        p.vy += p.gravity;
        p.x += p.vx;
        p.y += p.vy;
        p.opacity -= p.fadeSpeed;
        p.rotation += p.rotationSpeed;

        if (p.opacity > 0) {
          ctx.save();
          ctx.translate(p.x, p.y);
          ctx.rotate((p.rotation * Math.PI) / 180);
          ctx.globalAlpha = p.opacity;
          ctx.fillStyle = p.color;
          ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
          ctx.restore();
        } else {
          particles.splice(i, 1);
        }
      }
    }

    animationFrameId = requestAnimationFrame(renderParticles);
  }

  /**
   * فحص معلمات الرابط (?test=...) للتحكم في الحالات للاختبار (محلياً فقط)
   */
  function handleUrlOverrides() {
    if (isVisitorMode()) {
      if (elements.devTestPanel) {
        elements.devTestPanel.remove();
      }
      return;
    }

    const params = new URLSearchParams(window.location.search);
    const testMode = params.get('test') || params.get('preview') || params.get('state');

    if (testMode === 'ended' || testMode === 'zero' || testMode === 'celebration') {
      simulatedTargetTime = Date.now() - 1000;
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: تجربة عند الصفر (عبر الرابط)";
      setActiveDevButton(elements.btnTestZero);
    } else if (testMode === '3s' || testMode === '5s' || testMode === 'countdown') {
      const secs = testMode === '3s' ? 3000 : 5000;
      simulatedTargetTime = Date.now() + secs;
      if (elements.devStatusText) elements.devStatusText.textContent = `الحالة: تجربة عدّاد ${secs/1000} ثوانٍ`;
      setActiveDevButton(elements.btnTest3Sec);
    } else if (testMode === 'album' || testMode === 'letter') {
      simulatedTargetTime = Date.now() - 1000;
      triggerCelebration(false);
      openAlbumModal(0);
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: الجواب مفتوح مباشرة";
      setActiveDevButton(elements.btnTestAlbumDirect);
    }
  }

  /**
   * إعداد لوحة أدوات المراجعة المحلية
   */
  function setupDevPanel() {
    if (!elements.devTestPanel) return;

    if (isVisitorMode()) {
      elements.devTestPanel.remove();
      return;
    }

    if (elements.devToggleBtn) {
      elements.devToggleBtn.addEventListener('click', () => {
        elements.devTestPanel.classList.toggle('open');
      });
    }

    if (elements.btnTestNormal) {
      elements.btnTestNormal.addEventListener('click', () => {
        simulatedTargetTime = null;
        setActiveDevButton(elements.btnTestNormal);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: التوقيت الفعلي (قبل الموعد)";
        resetToCountdown();
      });
    }

    if (elements.btnTest3Sec) {
      elements.btnTest3Sec.addEventListener('click', () => {
        simulatedTargetTime = Date.now() + 3000;
        setActiveDevButton(elements.btnTest3Sec);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: تجربة ٣ ثوانٍ للصفر";
        resetToCountdown();
      });
    }

    if (elements.btnTestZero) {
      elements.btnTestZero.addEventListener('click', () => {
        simulatedTargetTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestZero);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: معاينة عند الصفر (الظرف والختم)";
        triggerCelebration(true);
      });
    }

    if (elements.btnTestAlbumDirect) {
      elements.btnTestAlbumDirect.addEventListener('click', () => {
        simulatedTargetTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestAlbumDirect);
        triggerCelebration(false);
        openAlbumModal(0);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: الجواب مفتوح مباشرة";
      });
    }
  }

  function setActiveDevButton(btn) {
    [elements.btnTestNormal, elements.btnTest3Sec, elements.btnTestZero, elements.btnTestAlbumDirect].forEach(b => {
      if (b) b.classList.remove('active');
    });
    if (btn) btn.classList.add('active');
  }

  /**
   * بدء التشغيل
   */
  function init() {
    applyConfiguration();
    setupEnvelopeEvents();
    setupAlbumEvents();
    handleUrlOverrides();
    setupDevPanel();
    initSparklesCanvas();

    updateCountdownDisplay();
    if (!isCelebrationActive) {
      timerInterval = setInterval(updateCountdownDisplay, 1000);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
