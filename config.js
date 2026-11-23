/**
 * Birthday Surprise Configuration - إعدادات مفاجأة عيد الميلاد
 * Designed for easy edits - قابلة للتعديل بسهولة
 */
const BIRTHDAY_CONFIG = {
  // الموعد المستهدف: بداية يوم ٢ ديسمبر ٢٠٢٦، الساعة ٠٠:٠٠ بتوقيت القاهرة (UTC+02:00)
  targetDateCairo: "2026-12-02T00:00:00+02:00",

  // النصوص الرئيسية
  title: "يا رفووووووق ❤️",
  subtitle: "فاضل شوية على عيد ميلادك… وقبل ما ييجي، عايز أرجع معاكي ليوم بحبه أوي",
  
  // نصوص الصورة والذكرى
  photoDateBadge: "٢٣ نوفمبر",
  photoMemoryCaption: "فاكرة يوم ما أبونا صلّى على الدبل، وبعدها نزلنا أول ديت؟ كل ما ببص للصورة دي ببتسم",

  // رسالة انتهاء العدّاد عند الصفر
  birthdayCelebrationTitle: "كل سنة وإنتِ طيبة يا رفووووووق ❤️",
  birthdayCelebrationSubtitle: "يا رب كل سنة وإحنا سوا وفي حضن بعض، ودايمًا منورة حياتي ومفرّحة قلبي 💍✨",

  // مسار الصورة الافتتاحية (السيلفي القريبة مع الدبل)
  heroImage: "assets/images/hero-selfie-rings.jpg",

  // تسميات وحدات العدّاد
  timerLabels: {
    days: "يوم",
    hours: "ساعة",
    minutes: "دقيقة",
    seconds: "ثانية"
  },

  // صور الألبوم المخصصة للمرحلة اللاحقة
  albumPhotosPhaseTwo: [
    { id: 1, title: "صورة المراية", src: "assets/images/photo-1-mirror.jpg" },
    { id: 2, title: "سيلفي الدبل (صورة الافتتاح)", src: "assets/images/hero-selfie-rings.jpg" },
    { id: 3, title: "السيلفي الثانية بالدبل", src: "assets/images/photo-3-selfie-rings-2.jpg" },
    { id: 4, title: "الصورة الجماعية مع أبونا", src: "assets/images/photo-4-group-father.jpg" }
  ],

  // تفعيل أدوات الاختبار السريع عبر معلمات الرابط (?test=ended أو ?fast=true)
  allowUrlOverrides: true
};

// Make config globally available and exportable if used in modules
if (typeof module !== "undefined" && module.exports) {
  module.exports = BIRTHDAY_CONFIG;
}
