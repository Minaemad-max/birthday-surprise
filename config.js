/**
 * Birthday Surprise Configuration - إعدادات مفاجأة عيد الميلاد
 * Phase 3: Engagement Envelope & Memory Albums Edition
 * ظرف يوم خطوبتنا (٢٥ نوفمبر) + جواب حب وذكرى صلاة الدبل (٢٣ نوفمبر) + عدّاد عيد الميلاد (٢ ديسمبر)
 */
const BIRTHDAY_CONFIG = {
  // موعد فك قفل ظرف الخطوبة: بداية يوم ٢٥ نوفمبر ٢٠٢٦، الساعة ٠٠:٠٠ بتوقيت القاهرة (UTC+02:00)
  engagementDateCairo: "2026-11-25T00:00:00+02:00",

  // الموعد المستهدف لعيد الميلاد: بداية يوم ٢ ديسمبر ٢٠٢٦، الساعة ٠٠:٠٠ بتوقيت القاهرة (UTC+02:00)
  targetDateCairo: "2026-12-02T00:00:00+02:00",

  // النصوص الرئيسية لواجهة الاستقبال
  title: "يا رفووووووق ❤️",
  subtitle: "فاضل شوية على عيد ميلادك… وقبل ما ييجي، عايز أرجع معاكي ليوم بحبه أوي",
  
  // نصوص الصورة والذكرى في واجهة الاستقبال (صورة ٢٣ نوفمبر)
  photoDateBadge: "٢٣ نوفمبر",
  photoMemoryCaption: "فاكرة يوم ما أبونا صلّى على الدبل، وبعدها نزلنا أول ديت؟ كل ما ببص للصورة دي ببتسم",

  // رسالة انتهاء العدّاد عند الصفر في عيد ميلادها (٢ ديسمبر)
  birthdayCelebrationTitle: "كل سنة وإنتِ طيبة يا رفووووووق ❤️",
  birthdayCelebrationSubtitle: "يا رب كل سنة وإحنا سوا وفي حضن بعض، ودايمًا منورة حياتي ومفرّحة قلبي 💍✨",

  // صورة الافتتاح (السيلفي القريبة مع الدبل)
  heroImage: "assets/images/hero-selfie-rings.jpg",

  // بيانات ظرف «يوم خطوبتنا» المستقل (ينفتح بداية ٢٥ نوفمبر)
  engagementEnvelope: {
    name: "يوم خطوبتنا",
    envelopeLabel: "لرفووووووق",
    lockedText: "يتفتح يوم ٢٥ نوفمبر",
    unlockedText: "متاح الآن للفتح ✨",
    buttonText: "افتحي ظرف الخطوبة",
    title: "يوم خطوبتنا",
    subtitle: "ألبوم ذكريات اليوم اللي لبسنا فيه الدبل وشاركنا أحلى فرحة سوا 💍✨",
    letterDedication: "يا رفووووووق، يوم ٢٥ نوفمبر مش مجرد تاريخ، ده اليوم اللي لبسنا فيه دبل بعض ووعدنا بعض نكمل العمر سوا 💍❤️",
    closingMessage: "أحلى خطوبة وأجمل بداية… وكل لحظة معاكي بتأكدلي إني اخترت صح. بحبك يا رفووووووق ❤️",
    signature: "بحبك",
    isAwaitingMorePhotos: true,
    awaitingPhotosNotice: "تم اعتماد أول صورة رسمية، وبانتظار باقي صور الخطوبة لاعتماد الألبوم النهائي."
  },

  // ألبوم صور الخطوبة (بترتيب الإرسال مع بدائل للمعاينة بانتظار باقي الصور)
  engagementPhotos: [
    {
      id: 1,
      title: "أحلى ليلة خطوبة",
      caption: "يوم خطوبتنا… اليوم اللي بدأنا فيه حكايتنا رسمي ولبسنا دبل بعض قدام الكل 💍💐",
      src: "assets/images/engagement-photo-1.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٥ نوفمبر",
      isOfficial: true
    },
    {
      id: 2,
      title: "لقطة ثانية من الخطوبة",
      caption: "ضحكتنا وفرحتنا في ليلة العمر (صورة للمعاينة المحلية بانتظار باقي صور الخطوبة) ✨",
      src: "assets/images/engagement-photo-1.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٥ نوفمبر",
      isPlaceholder: true,
      placeholderHint: "بانتظار استلام باقي الصور"
    }
  ],

  // بيانات جواب الحب وظرف ٢٣ نوفمبر (ينفتح مع عيد الميلاد ٢ ديسمبر)
  envelope: {
    name: "ظرف ٢٣ نوفمبر",
    envelopeLabel: "لرفووووووق",
    buttonText: "افتحي الجواب يا رفووووووق",
    subtitle: "ألبوم ذكريات يوم صلاة الدبل وأول ديت سوا",
    letterDedication: "يا رفووووووق، لو هختار يوم أعيشه معاكي تاني، يوم ٢٣ نوفمبر هييجي في بالي على طول. ❤️",
    closingMessage: "يوم ٢٣ نوفمبر كان حلو أوي عشان كنت معاكي… وكل سنة وإنتِ حبيبتي يا رفووووووق ❤️",
    signature: "بحبك"
  },

  // ألبوم صور ٢٣ نوفمبر الأربع بترتيب الحكاية
  albumPhotos: [
    {
      id: 1,
      title: "الصورة الجماعية مع أبونا",
      caption: "يوم ما أبونا صلّى على الدبل",
      src: "assets/images/photo-4-group-father.jpg",
      isGroupPhoto: true, // لضمان ظهور كل الأشخاص دون اقتطاع
      dateBadge: "٢٣ نوفمبر"
    },
    {
      id: 2,
      title: "صورة المراية",
      caption: "أنا وإنتِ يوم ٢٣ نوفمبر",
      src: "assets/images/photo-1-mirror.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٣ نوفمبر"
    },
    {
      id: 3,
      title: "السيلفي اللي في الافتتاح",
      caption: "وبعدها نزلنا أول ديت",
      src: "assets/images/hero-selfie-rings.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٣ نوفمبر"
    },
    {
      id: 4,
      title: "السيلفي التانية بالدبل",
      caption: "كل ما أبص للصور دي ببتسم. بحبك يا رفووووووق ❤️",
      src: "assets/images/photo-3-selfie-rings-2.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٣ نوفمبر"
    }
  ],

  // تسميات وحدات العدّاد
  timerLabels: {
    days: "يوم",
    hours: "ساعة",
    minutes: "دقيقة",
    seconds: "ثانية"
  },

  // نصوص أزرار ألبوم الذكريات
  albumNav: {
    prev: "السابق",
    next: "التالي",
    close: "إغلاق ✕",
    photoCounter: "صورة {current} من {total}"
  }
};

// Make config globally available and exportable if used in modules
if (typeof module !== "undefined" && module.exports) {
  module.exports = BIRTHDAY_CONFIG;
}
