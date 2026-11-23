/**
 * Birthday Surprise Configuration - إعدادات مفاجأة عيد الميلاد
 * النسخة المعتمدة - المرحلة الرابعة: افتتاحية عيد الميلاد، شخصية النجمة والتورتة، والأظرف المستقلة
 */
const BIRTHDAY_CONFIG = {
  // موعد فك قفل ظرف الخطوبة: بداية يوم ٢٥ مايو ٢٠٢٦، الساعة ٠٠:٠٠ بتوقيت رفووووووووووق (UTC+02:00)
  engagementDateCairo: "2026-11-25T00:00:00+02:00",

  // الموعد المستهدف لعيد الميلاد: بداية يوم ٢ ديسمبر ٢٠٢٦، الساعة ٠٠:٠٠ بتوقيت رفووووووووووق (UTC+02:00)
  targetDateCairo: "2026-12-02T00:00:00+02:00",

  // النصوص الرئيسية لواجهة الاستقبال
  title: "يا رفووووووق ❤️",
  subtitle: "فاضل شوية على عيد ميلادك… وقبل ما ييجي، عايز أرجع معاكي ليوم بحبه أوي",

  // نصوص الصورة والذكرى في واجهة الاستقبال (صورة ٢٣ مايو)
  photoDateBadge: "٢٣ مايو",
  photoMemoryCaption: "فاكرة يوم ما أبونا صلّى على الدبل، وبعدها نزلنا أول ديت؟ كل ما ببص للصورة دي ببتسم",

  // نصوص افتتاحية عيد الميلاد والشمعة والنجمة (٢ ديسمبر)
  birthdayCelebrationTitle: "كل سنة وإنتِ طيبة يا رفووووووق ❤️",
  birthdayCelebrationSubtitle: "يا رب السنة دي تضحكي فيها من قلبك كتير، وأنا أبقى جنبك في كل ضحكة",
  birthdayWishButtonText: "يا رفووووووق، عندك أمنية؟ 🎂",
  birthdayMakeWishText: "اتمنّي أمنية",
  birthdayMakeWishHint: "غمضي عينك للحظة، اتمني أمنية من قلبك… ودوسي تطفي الشمعة 🕯️",
  birthdayBlowCandleButtonText: "اطفي الشمعة",
  birthdayOpenLetterButtonText: "افتحي جواب عيد ميلادك",
  birthdaySkipAnimationText: "تخطي الحركة ⏭️",

  // قسم التسجيل الصوتي «اسمعيني» (يعمل بالضغط فقط عند توفر الملف)
  audioNote: {
    enabled: false, // يمكن تفعيله فور تسليم ملف الصوت
    title: "اسمعيني",
    subtitle: "رسالة صوتية من قلبي ليكي في عيد ميلادك ❤️",
    src: "assets/audio/voice-note.mp3"
  },

  // صورة الافتتاح (السيلفي القريبة مع الدبل)
  heroImage: "assets/images/hero-selfie-rings.jpg",

  // بيانات ظرف «يوم خطوبتنا» المستقل (ينفتح بداية ٢٥ مايو)
  engagementEnvelope: {
    name: "يوم خطوبتنا",
    envelopeLabel: "لرفووووووق",
    lockedText: "يتفتح يوم ٢٥ مايو",
    unlockedText: "متاح الآن للفتح ✨",
    buttonText: "افتحي ظرف الخطوبة",
    title: "يوم خطوبتنا",
    subtitle: "ألبوم ذكريات اليوم اللي لبسنا فيه الدبل وشاركنا أحلى فرحة سوا 💍✨",
    letterDedication: "يا رفووووووق، يوم ٢٥ مايو مش مجرد تاريخ، ده اليوم اللي لبسنا فيه دبل بعض ووعدنا بعض نكمل العمر سوا 💍❤️",
    closingMessage: "أحلى خطوبة وأجمل بداية… وكل لحظة معاكي بتأكدلي إني اخترت صح. بحبك يا رفووووووق ❤️",
    signature: "بحبك 🌹"
  },

  // ألبوم صورة الخطوبة المعتمدة الرسمية فقط (صورة واحدة)
  engagementPhotos: [
    {
      id: 1,
      title: "أحلى ليلة خطوبة",
      caption: "يوم خطوبتنا… اليوم اللي بدأنا فيه حكايتنا رسمي ولبسنا دبل بعض قدام الكل 💍💐",
      src: "assets/images/engagement-photo-1.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٥ مايو"
    }
  ],

  // بيانات جواب الحب وظرف ٢٣ مايو (ينفتح مع عيد الميلاد ٢ ديسمبر)
  envelope: {
    name: "ظرف ٢٣ مايو",
    envelopeLabel: "لرفووووووق",
    buttonText: "افتحي جواب عيد ميلادك",
    subtitle: "ألبوم ذكريات يوم صلاة الدبل وأول ديت سوا",
    letterDedication: "يا رفووووووق، لو هختار يوم أعيشه معاكي تاني، يوم ٢٣ مايو هييجي في بالي على طول. ❤️",
    closingMessage: "يوم ٢٣ مايو كان حلو أوي عشان كنت معاكي… وكل سنة وإنتِ حبيبتي يا رفووووووق ❤️",
    signature: "بحبك 🌹"
  },

  // ألبوم صور ٢٣ مايو الأربع بترتيب الحكاية بالصور الأصلية المعتمدة
  albumPhotos: [
    {
      id: 1,
      title: "الصورة الجماعية مع أبونا",
      caption: "يوم ما أبونا صلّى على الدبل",
      src: "assets/images/photo-4-group-father.jpg",
      isGroupPhoto: true, // لضمان ظهور كل الأشخاص دون اقتطاع في الكادر الأفقي
      dateBadge: "٢٣ مايو"
    },
    {
      id: 2,
      title: "صورة المراية",
      caption: "أنا وإنتِ يوم ٢٣ مايو",
      src: "assets/images/photo-1-mirror.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٣ مايو"
    },
    {
      id: 3,
      title: "السيلفي اللي في الافتتاح",
      caption: "وبعدها نزلنا أول ديت",
      src: "assets/images/hero-selfie-rings.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٣ مايو"
    },
    {
      id: 4,
      title: "السيلفي التانية بالدبل",
      caption: "كل ما أبص للصور دي ببتسم. بحبك يا رفووووووق ❤️",
      src: "assets/images/photo-3-selfie-rings-2.jpg",
      isGroupPhoto: false,
      dateBadge: "٢٣ مايو"
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
