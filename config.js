/**
 * Birthday Surprise Configuration - إعدادات مفاجأة عيد الميلاد
 * Phase 2 Romantic Edition: Love Letter & Roses - تجربة جواب الحب والورد
 */
const BIRTHDAY_CONFIG = {
  // الموعد المستهدف: بداية يوم ٢ ديسمبر ٢٠٢٦، الساعة ٠٠:٠٠ بتوقيت القاهرة (UTC+02:00)
  targetDateCairo: "2026-12-02T00:00:00+02:00",

  // النصوص الرئيسية
  title: "يا رفووووووق ❤️",
  subtitle: "فاضل شوية على عيد ميلادك… وقبل ما ييجي، عايز أرجع معاكي ليوم بحبه أوي",
  
  // نصوص الصورة والذكرى في واجهة الاستقبال
  photoDateBadge: "٢٣ نوفمبر",
  photoMemoryCaption: "فاكرة يوم ما أبونا صلّى على الدبل، وبعدها نزلنا أول ديت؟ كل ما ببص للصورة دي ببتسم",

  // رسالة انتهاء العدّاد عند الصفر
  birthdayCelebrationTitle: "كل سنة وإنتِ طيبة يا رفووووووق ❤️",
  birthdayCelebrationSubtitle: "يا رب كل سنة وإحنا سوا وفي حضن بعض، ودايمًا منورة حياتي ومفرّحة قلبي 💍✨",

  // صورة الافتتاح (السيلفي القريبة مع الدبل)
  heroImage: "assets/images/hero-selfie-rings.jpg",

  // بيانات جواب الحب وظرف ٢٣ نوفمبر
  envelope: {
    name: "ظرف ٢٣ نوفمبر",
    envelopeLabel: "لرفووووووق",
    buttonText: "افتحي الجواب يا رفووووووق",
    subtitle: "ألبوم ذكريات يوم صلاة الدبل وأول ديت سوا",
    letterDedication: "يا رفووووووق، لو هختار يوم أعيشه معاكي تاني، يوم ٢٣ نوفمبر هييجي في بالي على طول. ❤️",
    closingMessage: "يوم ٢٣ نوفمبر كان حلو أوي عشان كنت معاكي… وكل سنة وإنتِ حبيبتي يا رفووووووق ❤️",
    signature: "بحبك"
  },

  // ألبوم الصور الأربع بترتيب الحكاية
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
    close: "إغلاق الجواب ✕",
    photoCounter: "صورة {current} من {total}"
  }
};

// Make config globally available and exportable if used in modules
if (typeof module !== "undefined" && module.exports) {
  module.exports = BIRTHDAY_CONFIG;
}
