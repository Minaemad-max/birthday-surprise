/**
 * Birthday Surprise Engine - Phase 3: Engagement Envelope & Love Letter Albums
 * محرك موقع مفاجأة عيد ميلاد رفوووووق
 * - ظرف يوم خطوبتنا (مستقل - ينفتح بداية ٢٥ نوفمبر بتوقيت القاهرة)
 * - عدّاد عيد الميلاد (ينتهي مع بداية ٢ ديسمبر بتوقيت القاهرة)
 * - ظرف ٢٣ نوفمبر وجواب الحب وألبوم ذكريات صلاة الدبل (ينفتح عند الصفر في ٢ ديسمبر)
 * - دعم كامل للاستجابة على الموبايل، تقليل الحركة، وتحكم منفصل في الألبومات
 */

(function () {
  'use strict';

  // التحقق من وجود ملف الإعدادات
  const config = typeof BIRTHDAY_CONFIG !== 'undefined' ? BIRTHDAY_CONFIG : {
    engagementDateCairo: "2026-11-25T00:00:00+02:00",
    targetDateCairo: "2026-12-02T00:00:00+02:00",
    title: "يا رفووووووق ❤️",
    subtitle: "فاضل شوية على عيد ميلادك… وقبل ما ييجي، عايز أرجع معاكي ليوم بحبه أوي",
    photoDateBadge: "٢٣ نوفمبر",
    photoMemoryCaption: "فاكرة يوم ما أبونا صلّى على الدبل، وبعدها نزلنا أول ديت؟ كل ما ببص للصورة دي ببتسم",
    birthdayCelebrationTitle: "كل سنة وإنتِ طيبة يا رفووووووق ❤️",
    birthdayCelebrationSubtitle: "يا رب كل سنة وإحنا سوا وفي حضن بعض، ودايمًا منورة حياتي ومفرّحة قلبي 💍✨",
    heroImage: "assets/images/hero-selfie-rings.jpg",
    engagementEnvelope: {
      name: "يوم خطوبتنا",
      lockedText: "يتفتح يوم ٢٥ نوفمبر",
      buttonText: "افتحي ظرف الخطوبة",
      subtitle: "ألبوم ذكريات اليوم اللي لبسنا فيه الدبل وشاركنا أحلى فرحة سوا 💍✨",
      letterDedication: "يا رفووووووق، يوم ٢٥ نوفمبر مش مجرد تاريخ، ده اليوم اللي لبسنا فيه دبل بعض ووعدنا بعض نكمل العمر سوا 💍❤️",
      closingMessage: "أحلى خطوبة وأجمل بداية… وكل لحظة معاكي بتأكدلي إني اخترت صح. بحبك يا رفووووووق ❤️",
      signature: "بحبك"
    },
    engagementPhotos: [
      { id: 1, title: "أحلى ليلة خطوبة", caption: "يوم خطوبتنا… اليوم اللي بدأنا فيه حكايتنا رسمي ولبسنا دبل بعض قدام الكل 💍💐", src: "assets/images/engagement-photo-1.jpg", isGroupPhoto: false, dateBadge: "٢٥ نوفمبر" }
    ],
    envelope: {
      name: "ظرف ٢٣ نوفمبر",
      buttonText: "افتحي الجواب يا رفووووووق",
      subtitle: "ألبوم ذكريات يوم صلاة الدبل وأول ديت سوا",
      letterDedication: "يا رفووووووق، لو هختار يوم أعيشه معاكي تاني، يوم ٢٣ نوفمبر هييجي في بالي على طول. ❤️",
      closingMessage: "يوم ٢٣ نوفمبر كان حلو أوي عشان كنت معاكي… وكل سنة وإنتِ حبيبتي يا رفووووووق ❤️",
      signature: "بحبك"
    },
    albumPhotos: [
      { id: 1, title: "الصورة الجماعية مع أبونا", caption: "يوم ما أبونا صلّى على الدبل", src: "assets/images/photo-4-group-father.jpg", isGroupPhoto: true, dateBadge: "٢٣ نوفمبر" }
    ],
    timerLabels: { days: "يوم", hours: "ساعة", minutes: "دقيقة", seconds: "ثانية" }
  };

  // عناصر واجهة المستخدم
  const elements = {
    // ترويسة وصورة الافتتاح
    pageTitle: document.getElementById('pageTitle'),
    pageSubtitle: document.getElementById('pageSubtitle'),
    heroImage: document.getElementById('heroImage'),
    photoDateBadge: document.getElementById('photoDateBadge'),
    photoMemoryCaption: document.getElementById('photoMemoryCaption'),
    
    // عدّاد عيد الميلاد
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

    // مكوّنات افتتاحية عيد الميلاد وشخصية النجمة والتورتة (المرحلة 4)
    btnSkipAnimation: document.getElementById('btnSkipAnimation'),
    starStageContainer: document.getElementById('starStageContainer'),
    starCharacterWrap: document.getElementById('starCharacterWrap'),
    starEyesNormal: document.getElementById('starEyesNormal'),
    starEyesHappy: document.getElementById('starEyesHappy'),
    candleFlameGroup: document.getElementById('candleFlameGroup'),
    smokePuffGroup: document.getElementById('smokePuffGroup'),
    wishStepPrompt: document.getElementById('wishStepPrompt'),
    btnAskWish: document.getElementById('btnAskWish'),
    birthdayWishButtonText: document.getElementById('birthdayWishButtonText'),
    wishStepBlow: document.getElementById('wishStepBlow'),
    birthdayMakeWishText: document.getElementById('birthdayMakeWishText'),
    birthdayMakeWishHint: document.getElementById('birthdayMakeWishHint'),
    btnBlowCandle: document.getElementById('btnBlowCandle'),
    birthdayBlowCandleButtonText: document.getElementById('birthdayBlowCandleButtonText'),
    celebrationContentRevealed: document.getElementById('celebrationContentRevealed'),
    openBirthdayLetterBtn: document.getElementById('openBirthdayLetterBtn'),
    birthdayOpenLetterBtnText: document.getElementById('birthdayOpenLetterBtnText'),

    // قسم التسجيل الصوتي «اسمعيني»
    voiceNoteSection: document.getElementById('voiceNoteSection'),
    voiceNoteTitle: document.getElementById('voiceNoteTitle'),
    voiceNoteSubtitle: document.getElementById('voiceNoteSubtitle'),
    surpriseAudio: document.getElementById('surpriseAudio'),
    audioPlayBtn: document.getElementById('audioPlayBtn'),
    audioPlayIcon: document.getElementById('audioPlayIcon'),
    audioBtnLabel: document.getElementById('audioBtnLabel'),
    audioProgressBar: document.getElementById('audioProgressBar'),
    audioProgressFill: document.getElementById('audioProgressFill'),
    audioCurrentTime: document.getElementById('audioCurrentTime'),
    audioDuration: document.getElementById('audioDuration'),

    // مكوّنات ظرف يوم خطوبتنا (مستقل)
    engagementEnvelopeSection: document.getElementById('engagementEnvelopeSection'),
    engagementCard: document.getElementById('engagementCard'),
    engagementEnvelopeContainer: document.getElementById('engagementEnvelopeContainer'),
    engagementEnvelopeOuter: document.getElementById('engagementEnvelopeOuter'),
    engagementEnvelopeFlap: document.getElementById('engagementEnvelopeFlap'),
    engagementEnvelopeSeal: document.getElementById('engagementEnvelopeSeal'),
    engagementLockedBadge: document.getElementById('engagementLockedBadge'),
    engagementLockedText: document.getElementById('engagementLockedText'),
    openEngagementBtn: document.getElementById('openEngagementBtn'),
    engagementStatusDesc: document.getElementById('engagementStatusDesc'),
    engagementSectionSubtitle: document.getElementById('engagementSectionSubtitle'),

    // شاشة ألبوم الصور والجواب المنبثقة (مشتركة للألبومين مع دعم السياق)
    memoryAlbumOverlay: document.getElementById('memoryAlbumOverlay'),
    albumBackdrop: document.getElementById('albumBackdrop'),
    loveLetterCard: document.getElementById('loveLetterCard'),
    albumPrefaceCard: document.getElementById('albumPrefaceCard'),
    albumStampIcon: document.getElementById('albumStampIcon'),
    albumModalHeaderTag: document.getElementById('albumModalHeaderTag'),
    closeAlbumBtn: document.getElementById('closeAlbumBtn'),
    letterDedicationQuote: document.getElementById('letterDedicationQuote'),
    albumScrollPromptText: document.getElementById('albumScrollPromptText'),
    
    albumPhotoViewport: document.getElementById('albumPhotoViewport'),
    albumCurrentImg: document.getElementById('albumCurrentImg'),
    placeholderNoticeBadge: document.getElementById('placeholderNoticeBadge'),
    albumCurrentCaption: document.getElementById('albumCurrentCaption'),
    albumFrameDateBadge: document.getElementById('albumFrameDateBadge'),
    albumDateBadgeText: document.getElementById('albumDateBadgeText'),
    
    currentPhotoNum: document.getElementById('currentPhotoNum'),
    totalPhotosNum: document.getElementById('totalPhotosNum'),
    albumPhotoTitleHint: document.getElementById('albumPhotoTitleHint'),
    albumCounterPill: document.getElementById('albumCounterPill'),
    albumNavBar: document.getElementById('albumNavBar'),
    albumSwipeHint: document.getElementById('albumSwipeHint'),
    albumPrevBtn: document.getElementById('albumPrevBtn'),
    albumNextBtn: document.getElementById('albumNextBtn'),
    albumDotsContainer: document.getElementById('albumDotsContainer'),
    albumPhotoFrame: document.getElementById('albumPhotoFrame'),
    
    albumClosingLetter: document.getElementById('albumClosingLetter'),
    albumClosingMsg: document.getElementById('albumClosingMsg'),
    albumClosingSignature: document.getElementById('albumClosingSignature'),
    albumSignatureText: document.getElementById('albumSignatureText'),

    sparklesCanvas: document.getElementById('sparklesCanvas'),

    // أدوات المعاينة والاختبار للمطور
    devTestPanel: document.getElementById('devTestPanel'),
    devToggleBtn: document.getElementById('devToggleBtn'),
    btnTestNormal: document.getElementById('btnTestNormal'),
    btnTestNov25Live: document.getElementById('btnTestNov25Live'),
    btnTestNov25Unlocked: document.getElementById('btnTestNov25Unlocked'),
    btnTestDec2Live: document.getElementById('btnTestDec2Live'),
    btnTestWishPrompt: document.getElementById('btnTestWishPrompt'),
    btnTestWishBlow: document.getElementById('btnTestWishBlow'),
    btnTestBirthdayActive: document.getElementById('btnTestBirthdayActive'),
    btnTestEngagementModal: document.getElementById('btnTestEngagementModal'),
    btnTestNov23Modal: document.getElementById('btnTestNov23Modal'),
    devStatusText: document.getElementById('devStatusText')
  };

  // حالة النظام
  let timerInterval = null;
  let simulatedBirthdayTime = null;
  let simulatedEngagementTime = null;
  let isCelebrationActive = false;
  let isEngagementUnlocked = false;
  let hasTransitionedFromCountdown = false;
  let hasLaunchedPetals = false;
  let isOpeningEnvelope = false;
  let currentWishState = 'prompt'; // 'prompt' | 'blow' | 'revealed'

  // الألبوم النشط في الـ Modal ('engagement' أو 'nov23')
  let activeAlbumType = 'nov23';
  let currentAlbumIndex = 0;

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
   * تطبيق الإعدادات الأولية على واجهة المستخدم
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
    if (elements.birthdayWishButtonText && config.birthdayWishButtonText) {
      elements.birthdayWishButtonText.textContent = config.birthdayWishButtonText;
    }
    if (elements.birthdayMakeWishText && config.birthdayMakeWishText) {
      elements.birthdayMakeWishText.textContent = config.birthdayMakeWishText;
    }
    if (elements.birthdayMakeWishHint && config.birthdayMakeWishHint) {
      elements.birthdayMakeWishHint.textContent = config.birthdayMakeWishHint;
    }
    if (elements.birthdayBlowCandleButtonText && config.birthdayBlowCandleButtonText) {
      elements.birthdayBlowCandleButtonText.textContent = config.birthdayBlowCandleButtonText;
    }
    if (elements.birthdayOpenLetterBtnText && config.birthdayOpenLetterButtonText) {
      elements.birthdayOpenLetterBtnText.textContent = config.birthdayOpenLetterButtonText;
    }
    if (elements.btnSkipAnimation && config.birthdaySkipAnimationText) {
      const skipSpan = elements.btnSkipAnimation.querySelector('span');
      if (skipSpan) skipSpan.textContent = config.birthdaySkipAnimationText;
    }
    if (elements.openEnvelopeBtn && config.envelope && config.envelope.buttonText) {
      const btnText = elements.openEnvelopeBtn.querySelector('.btn-text');
      if (btnText) btnText.textContent = config.envelope.buttonText;
    }
    if (elements.openEngagementBtn && config.engagementEnvelope && config.engagementEnvelope.buttonText) {
      const btnText = elements.openEngagementBtn.querySelector('.btn-text');
      if (btnText) btnText.textContent = config.engagementEnvelope.buttonText;
    }
    if (elements.engagementLockedText && config.engagementEnvelope && config.engagementEnvelope.lockedText) {
      elements.engagementLockedText.textContent = config.engagementEnvelope.lockedText;
    }
    if (elements.engagementSectionSubtitle && config.engagementEnvelope && config.engagementEnvelope.subtitle) {
      elements.engagementSectionSubtitle.textContent = config.engagementEnvelope.subtitle;
    }
    if (config.timerLabels) {
      if (elements.daysLabel) elements.daysLabel.textContent = config.timerLabels.days || "يوم";
      if (elements.hoursLabel) elements.hoursLabel.textContent = config.timerLabels.hours || "ساعة";
      if (elements.minutesLabel) elements.minutesLabel.textContent = config.timerLabels.minutes || "دقيقة";
      if (elements.secondsLabel) elements.secondsLabel.textContent = config.timerLabels.seconds || "ثانية";
    }
  }

  /**
   * حساب الوقت المتبقي بالنسبة لموعد عيد الميلاد (٢ ديسمبر ٢٠٢٦ بتوقيت القاهرة)
   */
  function getRemainingBirthdayTime() {
    let targetMs;
    if (simulatedBirthdayTime !== null) {
      targetMs = simulatedBirthdayTime;
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

  /**
   * حساب حالة موعد فتح ظرف الخطوبة (٢٥ نوفمبر ٢٠٢٦ بتوقيت القاهرة)
   */
  function getRemainingEngagementTime() {
    let targetMs;
    if (simulatedEngagementTime !== null) {
      targetMs = simulatedEngagementTime;
    } else {
      targetMs = new Date(config.engagementDateCairo).getTime();
    }

    const nowMs = Date.now();
    const diffMs = targetMs - nowMs;

    if (diffMs <= 0) {
      return { total: 0, isZero: true };
    }
    return { total: diffMs, isZero: false };
  }

  function formatNumber(num) {
    return String(num).padStart(2, '0');
  }

  /**
   * تحديث حالة ظرف الخطوبة (مغلق قبل ٢٥ نوفمبر / متاح بعدها)
   * يتم استدعاؤها مع كل ثانية لتوفير الانتقال التلقائي إذا كانت الصفحة مفتوحة عند منتصف الليل
   */
  function updateEngagementEnvelopeState() {
    const engagementTime = getRemainingEngagementTime();

    if (engagementTime.isZero) {
      // وصل الموعد أو بعده: فك قفل ظرف الخطوبة
      if (!isEngagementUnlocked) {
        isEngagementUnlocked = true;
        unlockEngagementEnvelope(true);
      }
    } else {
      // قبل ٢٥ نوفمبر: قفل الظرف وإظهار الشارة المعتمدة
      if (isEngagementUnlocked) {
        isEngagementUnlocked = false;
      }
      lockEngagementEnvelope();
    }
  }

  /**
   * فك قفل ظرف الخطوبة وإظهار زر «افتحي ظرف الخطوبة»
   */
  function unlockEngagementEnvelope(animate = false) {
    if (elements.engagementLockedBadge) {
      elements.engagementLockedBadge.classList.add('hidden');
    }
    if (elements.openEngagementBtn) {
      elements.openEngagementBtn.classList.remove('hidden');
    }
    if (elements.engagementStatusDesc) {
      elements.engagementStatusDesc.textContent = "جاهز للفتح الآن! اضغطي لفتح ألبوم ذكريات يوم خطوبتنا 💍✨";
    }
    if (elements.engagementEnvelopeOuter) {
      elements.engagementEnvelopeOuter.classList.remove('is-locked');
      elements.engagementEnvelopeOuter.setAttribute('title', 'اضغطي لفتح ظرف يوم خطوبتنا');
    }
  }

  /**
   * قفل ظرف الخطوبة وإظهار شارة «يتفتح يوم ٢٥ نوفمبر»
   */
  function lockEngagementEnvelope() {
    if (elements.engagementLockedBadge) {
      elements.engagementLockedBadge.classList.remove('hidden');
    }
    if (elements.openEngagementBtn) {
      elements.openEngagementBtn.classList.add('hidden');
    }
    if (elements.engagementStatusDesc) {
      elements.engagementStatusDesc.textContent = "ظرف خاص بذكرى يوم خطوبتنا… هيتفتح تلقائيًا مع بداية يوم ٢٥ نوفمبر";
    }
    if (elements.engagementEnvelopeOuter) {
      elements.engagementEnvelopeOuter.classList.add('is-locked');
      elements.engagementEnvelopeOuter.classList.remove('is-open', 'is-breaking-seal');
      elements.engagementEnvelopeOuter.setAttribute('title', 'يتفتح يوم ٢٥ نوفمبر');
    }
  }

  /**
   * تحديث شاشة العدّاد التنازلي لعيد الميلاد (٢ ديسمبر)
   */
  function updateCountdownDisplay() {
    const time = getRemainingBirthdayTime();

    // تحديث ظرف الخطوبة دائماً
    updateEngagementEnvelopeState();

    if (time.isZero) {
      // الوصول إلى الصفر: عيد الميلاد
      if (elements.daysVal) elements.daysVal.textContent = "00";
      if (elements.hoursVal) elements.hoursVal.textContent = "00";
      if (elements.minutesVal) elements.minutesVal.textContent = "00";
      if (elements.secondsVal) elements.secondsVal.textContent = "00";

      if (elements.timerGrid) {
        elements.timerGrid.classList.add('zero-pulse');
      }

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
   * ضبط حالة افتتاحية عيد الميلاد والشمعة والنجمة
   * 'prompt'   -> سؤال الأمنية
   * 'blow'     -> تقريب التورتة + اتمني واطفي الشمعة
   * 'revealed' -> الشمعة انطفت + التهنئة وجواب عيد الميلاد
   */
  function setWishState(state, animate = true) {
    const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const shouldAnimate = animate && !prefersReduced;

    currentWishState = state;

    if (state === 'prompt') {
      if (elements.wishStepPrompt) elements.wishStepPrompt.classList.remove('hidden');
      if (elements.wishStepBlow) elements.wishStepBlow.classList.add('hidden');
      if (elements.celebrationContentRevealed) elements.celebrationContentRevealed.classList.add('hidden');

      if (elements.starCharacterWrap) elements.starCharacterWrap.classList.remove('is-approaching');
      if (elements.starEyesNormal) elements.starEyesNormal.classList.remove('hidden');
      if (elements.starEyesHappy) elements.starEyesHappy.classList.add('hidden');

      if (elements.candleFlameGroup) {
        elements.candleFlameGroup.classList.remove('is-extinguished', 'is-bright');
        elements.candleFlameGroup.style.display = '';
      }
      if (elements.smokePuffGroup) {
        elements.smokePuffGroup.classList.add('hidden');
        elements.smokePuffGroup.classList.remove('is-rising');
      }
      if (elements.btnSkipAnimation) elements.btnSkipAnimation.style.display = '';
    } else if (state === 'blow') {
      if (elements.starCharacterWrap) elements.starCharacterWrap.classList.add('is-approaching');
      if (elements.candleFlameGroup) elements.candleFlameGroup.classList.add('is-bright');

      if (elements.wishStepPrompt) elements.wishStepPrompt.classList.add('hidden');
      if (elements.wishStepBlow) elements.wishStepBlow.classList.remove('hidden');
      if (elements.celebrationContentRevealed) elements.celebrationContentRevealed.classList.add('hidden');
      if (elements.btnSkipAnimation) elements.btnSkipAnimation.style.display = '';
    } else if (state === 'revealed') {
      if (elements.wishStepPrompt) elements.wishStepPrompt.classList.add('hidden');
      if (elements.wishStepBlow) elements.wishStepBlow.classList.add('hidden');
      if (elements.celebrationContentRevealed) elements.celebrationContentRevealed.classList.remove('hidden');

      if (elements.starEyesNormal) elements.starEyesNormal.classList.add('hidden');
      if (elements.starEyesHappy) elements.starEyesHappy.classList.remove('hidden');

      if (elements.candleFlameGroup) {
        if (shouldAnimate) {
          elements.candleFlameGroup.classList.add('is-extinguished');
        } else {
          elements.candleFlameGroup.style.display = 'none';
        }
      }

      if (elements.smokePuffGroup && shouldAnimate) {
        elements.smokePuffGroup.classList.remove('hidden');
        elements.smokePuffGroup.classList.add('is-rising');
        setTimeout(() => {
          if (elements.smokePuffGroup) elements.smokePuffGroup.classList.add('hidden');
        }, 1600);
      }

      if (shouldAnimate) {
        launchRosePetals();
      }

      if (elements.btnSkipAnimation) elements.btnSkipAnimation.style.display = 'none';
    }
  }

  /**
   * تفعيل حالة الاحتفال عند الصفر في ٢ ديسمبر (مع بقاء ظرف الخطوبة متاحاً)
   */
  function triggerCelebration(animate = false) {
    if (isCelebrationActive) return;
    isCelebrationActive = true;

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

    // فحص تقليل الحركة
    const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReduced) {
      setWishState('revealed', false);
    } else {
      setWishState(currentWishState || 'prompt', animate);
    }

    // التأكد التام من أن ظرف الخطوبة يظل متاحاً
    unlockEngagementEnvelope(false);

    launchCelebrationParticles();
  }

  /**
   * إعادة ضبط العرض لحالة العد التنازلي النشط
   */
  function resetToCountdown() {
    isCelebrationActive = false;
    hasTransitionedFromCountdown = false;
    isOpeningEnvelope = false;
    currentWishState = 'prompt';

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

    setWishState('prompt', false);

    if (elements.envelopeOuter) {
      elements.envelopeOuter.classList.remove('is-open', 'is-breaking-seal');
    }

    if (elements.engagementEnvelopeOuter) {
      elements.engagementEnvelopeOuter.classList.remove('is-open', 'is-breaking-seal');
    }

    if (elements.memoryAlbumOverlay) {
      elements.memoryAlbumOverlay.classList.add('hidden');
    }

    updateCountdownDisplay();
  }

  /**
   * إعداد أحداث فتح الظرفين (ظرف الخطوبة وظرف ٢٣ نوفمبر) وتدفق الأمنية والشمعة
   */
  function setupEnvelopeEvents() {
    // -------------------------------------------------------------
    // ١. حدث فتح ظرف يوم خطوبتنا (مستقل)
    // -------------------------------------------------------------
    function executeOpenEngagementSequence() {
      // إذا كان الظرف مغلقاً لم يحن موعده، لا يفتح
      if (!isEngagementUnlocked) {
        return;
      }
      if (isOpeningEnvelope) return;
      isOpeningEnvelope = true;

      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      if (prefersReduced) {
        if (elements.engagementEnvelopeOuter) {
          elements.engagementEnvelopeOuter.classList.add('is-open');
        }
        openAlbumModal('engagement', 0);
        isOpeningEnvelope = false;
        return;
      }

      // حركة متسلسلة لظرف الخطوبة: تفكيك ختم القلب -> فتح الغطاء -> بتلات ورد رقيقة -> فتح الألبوم
      if (elements.engagementEnvelopeOuter) {
        elements.engagementEnvelopeOuter.classList.add('is-breaking-seal');
      }

      setTimeout(() => {
        if (elements.engagementEnvelopeOuter) {
          elements.engagementEnvelopeOuter.classList.add('is-open');
        }
      }, 200);

      setTimeout(() => {
        launchRosePetals();
      }, 350);

      setTimeout(() => {
        openAlbumModal('engagement', 0);
        isOpeningEnvelope = false;
      }, 650);
    }

    if (elements.openEngagementBtn) {
      elements.openEngagementBtn.addEventListener('click', executeOpenEngagementSequence);
    }
    if (elements.engagementEnvelopeOuter) {
      elements.engagementEnvelopeOuter.addEventListener('click', () => {
        if (isEngagementUnlocked) {
          executeOpenEngagementSequence();
        }
      });
      elements.engagementEnvelopeOuter.addEventListener('keydown', (e) => {
        if (isEngagementUnlocked && (e.key === 'Enter' || e.key === ' ')) {
          e.preventDefault();
          executeOpenEngagementSequence();
        }
      });
    }

    // -------------------------------------------------------------
    // ٢. حدث فتح ظرف ٢٣ نوفمبر وجواب الحب (المتاح مع عيد الميلاد)
    // -------------------------------------------------------------
    function executeOpenNov23Sequence() {
      if (isOpeningEnvelope) return;
      isOpeningEnvelope = true;

      const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      if (prefersReduced) {
        if (elements.envelopeOuter) {
          elements.envelopeOuter.classList.add('is-open');
        }
        openAlbumModal('nov23', 0);
        isOpeningEnvelope = false;
        return;
      }

      if (elements.envelopeOuter) {
        elements.envelopeOuter.classList.add('is-breaking-seal');
      }

      setTimeout(() => {
        if (elements.envelopeOuter) {
          elements.envelopeOuter.classList.add('is-open');
        }
      }, 200);

      setTimeout(() => {
        launchRosePetals();
      }, 350);

      setTimeout(() => {
        openAlbumModal('nov23', 0);
        isOpeningEnvelope = false;
      }, 650);
    }

    if (elements.openEnvelopeBtn) {
      elements.openEnvelopeBtn.addEventListener('click', executeOpenNov23Sequence);
    }
    if (elements.envelopeOuter) {
      elements.envelopeOuter.addEventListener('click', executeOpenNov23Sequence);
      elements.envelopeOuter.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          executeOpenNov23Sequence();
        }
      });
    }

    // زر «افتحي جواب عيد ميلادك» يقود مباشرة لنفس ظرف وجواب ٢٣ نوفمبر
    if (elements.openBirthdayLetterBtn) {
      elements.openBirthdayLetterBtn.addEventListener('click', executeOpenNov23Sequence);
    }

    // ربط أحداث تدفق الشمعة والأمنية
    if (elements.btnAskWish) {
      elements.btnAskWish.addEventListener('click', () => {
        setWishState('blow', true);
      });
    }

    if (elements.btnBlowCandle) {
      elements.btnBlowCandle.addEventListener('click', () => {
        setWishState('revealed', true);
      });
    }

    if (elements.btnSkipAnimation) {
      elements.btnSkipAnimation.addEventListener('click', () => {
        setWishState('revealed', false);
      });
    }
  }

  /**
   * إطلاق بتلات الورد على جانبي الشاشة وحول الإطار (مرة واحدة عند فتح أي ظرف)
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
      
      const isLeft = i % 2 === 0;
      const leftPercent = isLeft 
        ? Math.random() * 20 + 2
        : Math.random() * 20 + 78;

      const size = Math.random() * 12 + 12;
      const delay = Math.random() * 0.8;
      const duration = Math.random() * 1.5 + 2.5;

      petal.style.left = `${leftPercent}%`;
      petal.style.width = `${size}px`;
      petal.style.height = `${size * 1.25}px`;
      petal.style.animationDelay = `${delay}s`;
      petal.style.animationDuration = `${duration}s`;

      elements.petalsContainer.appendChild(petal);
    }

    setTimeout(() => {
      if (elements.petalsContainer) {
        elements.petalsContainer.innerHTML = '';
      }
      hasLaunchedPetals = false; // السماح بإطلاقها مرة أخرى عند فتح الظرف الآخر
    }, 4500);
  }

  /**
   * جلب مصفوفة الصور للألبوم النشط
   */
  function getActivePhotos() {
    if (activeAlbumType === 'engagement') {
      return config.engagementPhotos || [];
    }
    return config.albumPhotos || [];
  }

  /**
   * إعداد دوائر مؤشرات ألبوم الصور
   */
  function initAlbumDots() {
    if (!elements.albumDotsContainer) return;
    elements.albumDotsContainer.innerHTML = '';
    const photos = getActivePhotos();

    if (elements.totalPhotosNum) {
      elements.totalPhotosNum.textContent = String(photos.length);
    }

    photos.forEach((photo, idx) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = `album-dot ${idx === currentAlbumIndex ? 'active' : ''}`;
      dot.setAttribute('aria-label', `الانتقال إلى صورة ${idx + 1}`);
      dot.addEventListener('click', () => {
        showAlbumPhoto(idx);
      });
      elements.albumDotsContainer.appendChild(dot);
    });
  }

  /**
   * فتح نافذة ألبوم الذكريات وضبط المحتوى حسب نوع الظرف ('engagement' أو 'nov23')
   */
  function openAlbumModal(albumType = 'nov23', index = 0) {
    if (!elements.memoryAlbumOverlay) return;

    activeAlbumType = albumType;
    currentAlbumIndex = index;
    const photos = getActivePhotos();
    const isSinglePhoto = photos.length <= 1;

    // ضبط نصوص وتفاصيل الـ Modal حسب نوع الظرف
    if (albumType === 'engagement') {
      const env = config.engagementEnvelope || {};
      if (elements.albumModalHeaderTag) elements.albumModalHeaderTag.textContent = "💍 ظرف يوم خطوبتنا";
      if (elements.albumStampIcon) elements.albumStampIcon.innerHTML = '<span class="rose-emoji">💍</span>';
      if (elements.letterDedicationQuote) {
        elements.letterDedicationQuote.textContent = `«${(env.letterDedication || '').replace(/^[«»\s]+|[«»\s]+$/g, '')}»`;
      }
      if (elements.albumScrollPromptText) {
        elements.albumScrollPromptText.innerHTML = isSinglePhoto 
          ? '<span class="prompt-text">صورة يوم خطوبتنا المطبوعة جوا الجواب</span><span class="prompt-arrow">↓</span>'
          : '<span class="prompt-text">صور الخطوبة مطبوعة جوا الظرف… اقلبي وشوفيها واحدة واحدة</span><span class="prompt-arrow">↓</span>';
      }
      if (elements.albumPhotoTitleHint) {
        elements.albumPhotoTitleHint.textContent = "ذكرى ليلة خطوبتنا";
      }
      if (elements.albumDateBadgeText) {
        elements.albumDateBadgeText.textContent = "٢٥ نوفمبر";
      }
      if (elements.albumClosingMsg) {
        elements.albumClosingMsg.textContent = `«${(env.closingMessage || '').replace(/^[«»\s]+|[«»\s]+$/g, '')}»`;
      }
      if (elements.albumSignatureText) {
        elements.albumSignatureText.textContent = env.signature || "بحبك 🌹";
      }
    } else {
      const env = config.envelope || {};
      if (elements.albumModalHeaderTag) elements.albumModalHeaderTag.textContent = "💌 ظرف ٢٣ نوفمبر";
      if (elements.albumStampIcon) elements.albumStampIcon.innerHTML = '<span class="rose-emoji">🌹</span>';
      if (elements.letterDedicationQuote) {
        elements.letterDedicationQuote.textContent = `«${(env.letterDedication || '').replace(/^[«»\s]+|[«»\s]+$/g, '')}»`;
      }
      if (elements.albumScrollPromptText) {
        elements.albumScrollPromptText.innerHTML = '<span class="prompt-text">الصور مطبوعة جوا الجواب… اقلبي وشوفيها واحدة واحدة</span><span class="prompt-arrow">↓</span>';
      }
      if (elements.albumPhotoTitleHint) {
        elements.albumPhotoTitleHint.textContent = "ذكريات ٢٣ نوفمبر";
      }
      if (elements.albumDateBadgeText) {
        elements.albumDateBadgeText.textContent = "٢٣ نوفمبر";
      }
      if (elements.albumClosingMsg) {
        elements.albumClosingMsg.textContent = `«${(env.closingMessage || '').replace(/^[«»\s]+|[«»\s]+$/g, '')}»`;
      }
      if (elements.albumSignatureText) {
        elements.albumSignatureText.textContent = env.signature || "بحبك 🌹";
      }
    }

    // إخفاء أزرار التقليب وشريط العداد وتلميح السحب في حالة الصورة الواحدة
    if (isSinglePhoto) {
      if (elements.albumNavBar) elements.albumNavBar.classList.add('hidden');
      if (elements.albumSwipeHint) elements.albumSwipeHint.classList.add('hidden');
      if (elements.albumCounterPill) elements.albumCounterPill.classList.add('hidden');
    } else {
      if (elements.albumNavBar) elements.albumNavBar.classList.remove('hidden');
      if (elements.albumSwipeHint) elements.albumSwipeHint.classList.remove('hidden');
      if (elements.albumCounterPill) elements.albumCounterPill.classList.remove('hidden');
      initAlbumDots();
    }

    showAlbumPhoto(index);

    elements.memoryAlbumOverlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
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
   * عرض صورة محددة في الألبوم النشط
   */
  function showAlbumPhoto(index) {
    const photos = getActivePhotos();
    if (!photos.length) return;

    if (index < 0) index = 0;
    if (index >= photos.length) index = photos.length - 1;

    currentAlbumIndex = index;
    const photo = photos[index];

    if (elements.currentPhotoNum) {
      elements.currentPhotoNum.textContent = String(index + 1);
    }
    if (elements.totalPhotosNum) {
      elements.totalPhotosNum.textContent = String(photos.length);
    }

    if (elements.albumCurrentImg) {
      elements.albumCurrentImg.src = photo.src;
      elements.albumCurrentImg.alt = photo.title || photo.caption;
    }

    if (elements.albumCurrentCaption) {
      elements.albumCurrentCaption.textContent = photo.caption;
    }

    if (elements.albumDateBadgeText) {
      elements.albumDateBadgeText.textContent = photo.dateBadge || (activeAlbumType === 'engagement' ? "٢٥ نوفمبر" : "٢٣ نوفمبر");
    }

    // تخصيص العرض للصورة الجماعية لظهور كل الأشخاص
    if (elements.albumPhotoViewport) {
      if (photo.isGroupPhoto) {
        elements.albumPhotoViewport.classList.add('is-group-photo');
      } else {
        elements.albumPhotoViewport.classList.remove('is-group-photo');
      }
    }

    // تحديث أزرار التنقل (السابق / التالي)
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

    if (elements.albumPrevBtn) {
      elements.albumPrevBtn.addEventListener('click', () => {
        if (currentAlbumIndex > 0) {
          showAlbumPhoto(currentAlbumIndex - 1);
        }
      });
    }
    if (elements.albumNextBtn) {
      elements.albumNextBtn.addEventListener('click', () => {
        const photos = getActivePhotos();
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
        // في RTL، السهم لليسار هو للأمام (التالي)
        const photos = getActivePhotos();
        if (photos.length > 1 && currentAlbumIndex < photos.length - 1) {
          showAlbumPhoto(currentAlbumIndex + 1);
        }
      } else if (e.key === 'ArrowRight') {
        // في RTL، السهم لليمين هو للوراء (السابق)
        const photos = getActivePhotos();
        if (photos.length > 1 && currentAlbumIndex > 0) {
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
      const photos = getActivePhotos();
      if (photos.length <= 1) return;

      const swipeDistance = touchEndX - touchStartX;
      const minSwipe = 40;

      if (Math.abs(swipeDistance) < minSwipe) return;

      if (swipeDistance < 0) {
        if (currentAlbumIndex < photos.length - 1) {
          showAlbumPhoto(currentAlbumIndex + 1);
        }
      } else {
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
   * إعداد قسم التسجيل الصوتي «اسمعيني»
   * يعمل بضغطة زر عند توفر ملف الصوت، ويظل مكتوماً وخاملاً إن لم يتوفر
   */
  function setupAudioNote() {
    const audioCfg = config.audioNote;
    if (!audioCfg || !audioCfg.enabled) {
      if (elements.voiceNoteSection) elements.voiceNoteSection.classList.add('hidden');
      return;
    }

    if (elements.voiceNoteSection) elements.voiceNoteSection.classList.remove('hidden');
    if (elements.voiceNoteTitle && audioCfg.title) elements.voiceNoteTitle.textContent = audioCfg.title;
    if (elements.voiceNoteSubtitle && audioCfg.subtitle) elements.voiceNoteSubtitle.textContent = audioCfg.subtitle;

    if (!elements.surpriseAudio || !elements.audioPlayBtn) return;

    if (audioCfg.src) {
      elements.surpriseAudio.src = audioCfg.src;
    }

    elements.audioPlayBtn.addEventListener('click', () => {
      if (elements.surpriseAudio.paused) {
        const playPromise = elements.surpriseAudio.play();
        if (playPromise !== undefined) {
          playPromise.then(() => {
            if (elements.audioPlayIcon) elements.audioPlayIcon.textContent = '⏸️';
            if (elements.audioBtnLabel) elements.audioBtnLabel.textContent = 'إيقاف مؤقت';
          }).catch(err => {
            console.warn('Audio play request handled:', err);
          });
        }
      } else {
        elements.surpriseAudio.pause();
        if (elements.audioPlayIcon) elements.audioPlayIcon.textContent = '▶️';
        if (elements.audioBtnLabel) elements.audioBtnLabel.textContent = 'تشغيل الرسالة';
      }
    });

    elements.surpriseAudio.addEventListener('timeupdate', () => {
      if (!elements.surpriseAudio.duration) return;
      const progress = (elements.surpriseAudio.currentTime / elements.surpriseAudio.duration) * 100;
      if (elements.audioProgressFill) elements.audioProgressFill.style.width = `${progress}%`;
      if (elements.audioCurrentTime) elements.audioCurrentTime.textContent = formatAudioTime(elements.surpriseAudio.currentTime);
    });

    elements.surpriseAudio.addEventListener('loadedmetadata', () => {
      if (elements.audioDuration) elements.audioDuration.textContent = formatAudioTime(elements.surpriseAudio.duration);
    });

    elements.surpriseAudio.addEventListener('ended', () => {
      if (elements.audioPlayIcon) elements.audioPlayIcon.textContent = '▶️';
      if (elements.audioBtnLabel) elements.audioBtnLabel.textContent = 'إعادة التشغيل';
      if (elements.audioProgressFill) elements.audioProgressFill.style.width = '100%';
    });

    if (elements.audioProgressBar) {
      elements.audioProgressBar.addEventListener('click', (e) => {
        if (!elements.surpriseAudio.duration) return;
        const rect = elements.audioProgressBar.getBoundingClientRect();
        const pos = (e.clientX - rect.left) / rect.width;
        elements.surpriseAudio.currentTime = Math.max(0, Math.min(pos * elements.surpriseAudio.duration, elements.surpriseAudio.duration));
      });
    }
  }

  function formatAudioTime(secs) {
    if (isNaN(secs) || secs < 0) return '0:00';
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  }

  /**
   * فحص معلمات الرابط (?test=...) للتحكم في الحالات للاختبار المؤتمت
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

    if (testMode === 'normal' || testMode === 'before_nov25') {
      simulatedBirthdayTime = null;
      simulatedEngagementTime = null;
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: التوقيت الفعلي (قبل ٢٥ نوفمبر)";
      setActiveDevButton(elements.btnTestNormal);
    } else if (testMode === 'nov25_live') {
      // تجربة عبور ليل ٢٥ نوفمبر بعد ٣ ثوانٍ
      simulatedEngagementTime = Date.now() + 3000;
      simulatedBirthdayTime = Date.now() + 600000;
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: تجربة عبور منتصف ليل ٢٥ نوفمبر بعد ٣ ثوانٍ";
      setActiveDevButton(elements.btnTestNov25Live);
    } else if (testMode === 'nov25_unlocked' || testMode === 'after_nov25') {
      // محاكاة ما بعد ٢٥ نوفمبر وقبل ٢ ديسمبر
      simulatedEngagementTime = Date.now() - 1000;
      simulatedBirthdayTime = Date.now() + 600000;
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: بعد ٢٥ نوفمبر (ظرف الخطوبة متاح والعدّاد يعمل)";
      setActiveDevButton(elements.btnTestNov25Unlocked);
    } else if (testMode === 'dec2_live' || testMode === '3s') {
      // تجربة عبور ليل ٢ ديسمبر بعد ٣ ثوانٍ
      simulatedEngagementTime = Date.now() - 1000;
      simulatedBirthdayTime = Date.now() + 3000;
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: تجربة عبور ليل ٢ ديسمبر بعد ٣ ثوانٍ";
      setActiveDevButton(elements.btnTestDec2Live);
    } else if (testMode === 'wish_prompt' || testMode === 'step1') {
      simulatedEngagementTime = Date.now() - 2000;
      simulatedBirthdayTime = Date.now() - 1000;
      triggerCelebration(false);
      setWishState('prompt', false);
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: المرحلة ١ (سؤال الأمنية 🎂)";
      setActiveDevButton(elements.btnTestWishPrompt);
    } else if (testMode === 'wish_blow' || testMode === 'step2') {
      simulatedEngagementTime = Date.now() - 2000;
      simulatedBirthdayTime = Date.now() - 1000;
      triggerCelebration(false);
      setWishState('blow', false);
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: المرحلة ٢ (اتمني واطفي الشمعة 🕯️)";
      setActiveDevButton(elements.btnTestWishBlow);
    } else if (testMode === 'after_dec2' || testMode === 'zero' || testMode === 'celebration' || testMode === 'birthday_revealed' || testMode === 'step3') {
      // محاكاة عيد الميلاد والمرحلة الثالثة
      simulatedEngagementTime = Date.now() - 2000;
      simulatedBirthdayTime = Date.now() - 1000;
      triggerCelebration(false);
      setWishState('revealed', false);
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: بعد ٢ ديسمبر (المرحلة ٣: ظهور التهنئة والأظرف)";
      setActiveDevButton(elements.btnTestBirthdayActive);
    } else if (testMode === 'open_engagement' || testMode === 'engagement') {
      simulatedEngagementTime = Date.now() - 1000;
      unlockEngagementEnvelope(false);
      openAlbumModal('engagement', 0);
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: ظرف الخطوبة مفتوح مباشرة";
      setActiveDevButton(elements.btnTestEngagementModal);
    } else if (testMode === 'open_nov23' || testMode === 'album' || testMode === 'letter') {
      simulatedBirthdayTime = Date.now() - 1000;
      triggerCelebration(false);
      openAlbumModal('nov23', 0);
      if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: ظرف ٢٣ نوفمبر مفتوح مباشرة";
      setActiveDevButton(elements.btnTestNov23Modal);
    }
  }

  /**
   * إعداد لوحة أدوات المراجعة السريعة للمطور
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
        simulatedBirthdayTime = null;
        simulatedEngagementTime = null;
        setActiveDevButton(elements.btnTestNormal);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: التوقيت الفعلي (قبل ٢٥ نوفمبر - مقفول)";
        resetToCountdown();
      });
    }

    if (elements.btnTestNov25Live) {
      elements.btnTestNov25Live.addEventListener('click', () => {
        simulatedEngagementTime = Date.now() + 3000;
        simulatedBirthdayTime = Date.now() + 600000;
        setActiveDevButton(elements.btnTestNov25Live);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: عبور ليل ٢٥ نوفمبر (٣ ثوانٍ للفتح التلقائي)";
        resetToCountdown();
      });
    }

    if (elements.btnTestNov25Unlocked) {
      elements.btnTestNov25Unlocked.addEventListener('click', () => {
        simulatedEngagementTime = Date.now() - 1000;
        simulatedBirthdayTime = Date.now() + 600000;
        setActiveDevButton(elements.btnTestNov25Unlocked);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: بعد ٢٥ نوفمبر (ظرف الخطوبة متاح)";
        resetToCountdown();
      });
    }

    if (elements.btnTestDec2Live) {
      elements.btnTestDec2Live.addEventListener('click', () => {
        simulatedEngagementTime = Date.now() - 1000;
        simulatedBirthdayTime = Date.now() + 3000;
        setActiveDevButton(elements.btnTestDec2Live);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: عبور ليل ٢ ديسمبر (٣ ثوانٍ للصفر)";
        resetToCountdown();
      });
    }

    if (elements.btnTestWishPrompt) {
      elements.btnTestWishPrompt.addEventListener('click', () => {
        simulatedEngagementTime = Date.now() - 2000;
        simulatedBirthdayTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestWishPrompt);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: المرحلة ١ (سؤال الأمنية 🎂)";
        triggerCelebration(false);
        setWishState('prompt', false);
      });
    }

    if (elements.btnTestWishBlow) {
      elements.btnTestWishBlow.addEventListener('click', () => {
        simulatedEngagementTime = Date.now() - 2000;
        simulatedBirthdayTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestWishBlow);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: المرحلة ٢ (اتمني واطفي الشمعة 🕯️)";
        triggerCelebration(false);
        setWishState('blow', false);
      });
    }

    if (elements.btnTestBirthdayActive) {
      elements.btnTestBirthdayActive.addEventListener('click', () => {
        simulatedEngagementTime = Date.now() - 2000;
        simulatedBirthdayTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestBirthdayActive);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: بعد ٢ ديسمبر (المرحلة ٣: ظهور التهنئة والأظرف)";
        triggerCelebration(true);
        setWishState('revealed', false);
      });
    }

    if (elements.btnTestEngagementModal) {
      elements.btnTestEngagementModal.addEventListener('click', () => {
        simulatedEngagementTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestEngagementModal);
        unlockEngagementEnvelope(false);
        openAlbumModal('engagement', 0);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: فتح ألبوم الخطوبة مباشرة";
      });
    }

    if (elements.btnTestNov23Modal) {
      elements.btnTestNov23Modal.addEventListener('click', () => {
        simulatedBirthdayTime = Date.now() - 1000;
        setActiveDevButton(elements.btnTestNov23Modal);
        triggerCelebration(false);
        openAlbumModal('nov23', 0);
        if (elements.devStatusText) elements.devStatusText.textContent = "الحالة: فتح ظرف ٢٣ نوفمبر مباشرة";
      });
    }
  }

  function setActiveDevButton(btn) {
    const allBtns = [
      elements.btnTestNormal,
      elements.btnTestNov25Live,
      elements.btnTestNov25Unlocked,
      elements.btnTestDec2Live,
      elements.btnTestWishPrompt,
      elements.btnTestWishBlow,
      elements.btnTestBirthdayActive,
      elements.btnTestEngagementModal,
      elements.btnTestNov23Modal
    ];
    allBtns.forEach(b => {
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
    setupAudioNote();
    handleUrlOverrides();
    setupDevPanel();
    initSparklesCanvas();

    updateCountdownDisplay();
    timerInterval = setInterval(updateCountdownDisplay, 1000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
