/**
 * Birthday Surprise Engine - Phase 1
 * محرك موقع مفاجأة عيد ميلاد رفوووووق
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

    sparklesCanvas: document.getElementById('sparklesCanvas'),

    // أدوات الاختبار
    devTestPanel: document.getElementById('devTestPanel'),
    devToggleBtn: document.getElementById('devToggleBtn'),
    btnTestNormal: document.getElementById('btnTestNormal'),
    btnTest5Sec: document.getElementById('btnTest5Sec'),
    btnTestZero: document.getElementById('btnTestZero'),
    devStatusText: document.getElementById('devStatusText')
  };

  // حالة النظام
  let timerInterval = null;
  let simulatedTargetTime = null;
  let isCelebrationActive = false;

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
      if (textSpan) {
        textSpan.textContent = config.photoDateBadge;
      }
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
    if (config.timerLabels) {
      if (elements.daysLabel) elements.daysLabel.textContent = config.timerLabels.days || "يوم";
      if (elements.hoursLabel) elements.hoursLabel.textContent = config.timerLabels.hours || "ساعة";
      if (elements.minutesLabel) elements.minutesLabel.textContent = config.timerLabels.minutes || "دقيقة";
      if (elements.secondsLabel) elements.secondsLabel.textContent = config.timerLabels.seconds || "ثانية";
    }
  }

  /**
   * حساب الوقت المتبقي بالنسبة لتوقيت القاهرة الثابت (+02:00)
   */
  function getRemainingTime() {
    // الوقت المستهدف بالمللي ثانية UTC
    let targetMs;

    if (simulatedTargetTime !== null) {
      targetMs = simulatedTargetTime;
    } else {
      // التاريخ محدد بالمنطقة الزمنية للقاهرة (+02:00)
      targetMs = new Date(config.targetDateCairo).getTime();
    }

    // الوقت الحالي بالمللي ثانية UTC على جهاز الزائرة
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

  /**
   * تنسيق الأرقام مع الحفاظ على ثابت العرض
   */
  function formatNumber(num) {
    return String(num).padStart(2, '0');
  }

  /**
   * تحديث واجهة العدّاد
   */
  function updateCountdownDisplay() {
    const time = getRemainingTime();

    if (time.isZero) {
      triggerCelebration();
      return;
    }

    if (elements.daysVal) elements.daysVal.textContent = formatNumber(time.days);
    if (elements.hoursVal) elements.hoursVal.textContent = formatNumber(time.hours);
    if (elements.minutesVal) elements.minutesVal.textContent = formatNumber(time.minutes);
    if (elements.secondsVal) elements.secondsVal.textContent = formatNumber(time.seconds);
  }

  /**
   * تفعيل حالة الاحتفال عند الصفر
   */
  function triggerCelebration() {
    if (isCelebrationActive) return;
    isCelebrationActive = true;

    if (timerInterval) {
      clearInterval(timerInterval);
      timerInterval = null;
    }

    // إخفاء كارت العدّاد
    if (elements.countdownSection) {
      elements.countdownSection.style.opacity = '0';
      elements.countdownSection.style.transform = 'translateY(-10px)';
      setTimeout(() => {
        elements.countdownSection.style.display = 'none';
      }, 400);
    }

    // إظهار كارت الاحتفال
    if (elements.celebrationSection) {
      setTimeout(() => {
        elements.celebrationSection.classList.remove('hidden');
        elements.celebrationSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 350);
    }

    // إطلاق تأثير القلوب والألعاب النارية والنجوم
    launchCelebrationParticles();
  }

  /**
   * إعادة ضبط العرض لحالة العد التنازلي النشط
   */
  function resetToCountdown() {
    isCelebrationActive = false;

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

    if (timerInterval) {
      clearInterval(timerInterval);
    }

    updateCountdownDisplay();
    timerInterval = setInterval(updateCountdownDisplay, 1000);
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

    // إنشاء جزيئات الغبار الذهبي والنجوم الهادئة
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

    // إضافة 70 جسيم احتفالي (قلوب، نجوم لامعة، قصاصات ذهبية)
    for (let i = 0; i < 70; i++) {
      particles.push({
        type: Math.random() > 0.5 ? 'heart' : 'confetti',
        x: canvas.width * 0.5 + (Math.random() - 0.5) * 180,
        y: canvas.height * 0.4 + (Math.random() - 0.5) * 100,
        size: Math.random() * 8 + 6,
        vx: (Math.random() - 0.5) * 8,
        vy: -Math.random() * 9 - 4,
        gravity: 0.18,
        rotation: Math.random() * 360,
        rotationSpeed: (Math.random() - 0.5) * 8,
        opacity: 1,
        fadeSpeed: Math.random() * 0.008 + 0.003,
        color: ['#e5c378', '#ffd880', '#e85973', '#ffffff', '#ff9eb1'][Math.floor(Math.random() * 5)]
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
          // رسم شكل قلب صغير
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
   * فحص معلمات الرابط (?test=...) للتحكم في الحالات للاختبار
   */
  function handleUrlOverrides() {
    const params = new URLSearchParams(window.location.search);
    const testMode = params.get('test') || params.get('preview') || params.get('state');

    if (testMode === 'ended' || testMode === 'zero' || testMode === 'celebration') {
      simulatedTargetTime = Date.now() - 1000;
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: تجربة عند الصفر (عبر الرابط)";
      setActiveDevButton(elements.btnTestZero);
    } else if (testMode === '5s' || testMode === 'countdown') {
      simulatedTargetTime = Date.now() + 5000;
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: تجربة ٥ ثوانٍ للصفر (عبر الرابط)";
      setActiveDevButton(elements.btnTest5Sec);
    }
  }

  /**
   * إعداد لوحة أدوات المراجعة
   */
  function setupDevPanel() {
    if (!elements.devTestPanel) return;

    if (elements.devToggleBtn) {
      elements.devToggleBtn.addEventListener('click', () => {
        elements.devTestPanel.classList.toggle('open');
      });
    }

    if (elements.btnTestNormal) {
      elements.btnTestNormal.addEventListener('click', () => {
        simulatedTargetTime = null;
        setActiveDevButton(elements.btnTestNormal);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: التوقيت الفعلي (٨ أيام)";
        resetToCountdown();
      });
    }

    if (elements.btnTest5Sec) {
      elements.btnTest5Sec.addEventListener('click', () => {
        simulatedTargetTime = Date.now() + 5000;
        setActiveDevButton(elements.btnTest5Sec);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: تجربة عد ٥ ثوانٍ للصفر";
        resetToCountdown();
      });
    }

    if (elements.btnTestZero) {
      elements.btnTestZero.addEventListener('click', () => {
        simulatedTargetTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestZero);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: معاينة عند الصفر (الاحتفال)";
        triggerCelebration();
      });
    }
  }

  function setActiveDevButton(btn) {
    [elements.btnTestNormal, elements.btnTest5Sec, elements.btnTestZero].forEach(b => {
      if (b) b.classList.remove('active');
    });
    if (btn) btn.classList.add('active');
  }

  /**
   * بدء التشغيل
   */
  function init() {
    applyConfiguration();
    handleUrlOverrides();
    setupDevPanel();
    initSparklesCanvas();

    // بدء العدّاد فوراً
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
