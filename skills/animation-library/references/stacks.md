# Pola animasi per stack

Panduan singkat: kapan pakai stack yang mana, dan bagaimana pola idiomatisnya. `stack` di `index.json` harus salah satu dari: `vanilla-css`, `vanilla-js`, `tailwind`, `gsap`, `framer-motion`.

## vanilla-css (default)

Paling portable — jalan di project apa pun tanpa dependency tambahan. Pilih ini kecuali user jelas-jelas pakai stack lain di project mereka.

```css
@keyframes anim-fade-in-slow {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.anim-fade-in-slow {
  --duration: 0.8s;
  --ease: cubic-bezier(0.16, 1, 0.3, 1);
  animation: anim-fade-in-slow var(--duration) var(--ease) forwards;
}

@media (prefers-reduced-motion: reduce) {
  .anim-fade-in-slow { animation-duration: 0.01ms !important; }
}
```

## vanilla-js

Dipakai kalau animasinya butuh logika (trigger on-scroll pakai IntersectionObserver, animasi berbasis interaksi, atau timing yang tidak bisa murni CSS). Tetap manipulasi `transform`/`opacity`/class saja dari JS-nya; jangan animasikan properti layout langsung dari `requestAnimationFrame` kalau CSS transition/animation sudah cukup.

```js
const el = document.querySelector('.anim-target');
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) entry.target.classList.add('anim-fade-in-slow');
  });
}, { threshold: 0.2 });
observer.observe(el);
```

## tailwind

Kalau project sudah pakai Tailwind, prefer utility/arbitrary values dan `tailwind.config.js` `keyframes`/`animation` extension daripada nulis CSS terpisah, supaya konsisten dengan cara project itu sudah bekerja.

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      keyframes: {
        'fade-in-slow': {
          '0%':   { opacity: 0, transform: 'translateY(16px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
      animation: {
        'fade-in-slow': 'fade-in-slow 0.8s cubic-bezier(0.16,1,0.3,1) forwards',
      },
    },
  },
};
```

```html
<div class="animate-fade-in-slow">...</div>
```

Kalau user tidak mau/tidak bisa ubah config (mis. cuma butuh cepat di satu tempat), pakai arbitrary value: `class="[animation:fade-in-slow_0.8s_ease-out]"` plus keyframes tetap didefinisikan di CSS.

## gsap

Untuk animasi JS yang lebih kompleks (timeline, stagger banyak elemen, scroll-trigger canggih). Jangan pakai GSAP untuk animasi simpel yang CSS saja sudah cukup — overhead-nya tidak sepadan.

```js
import gsap from "gsap";

gsap.from(".anim-target", {
  opacity: 0,
  y: 16,
  duration: 0.8,
  ease: "power3.out",
});
```

## framer-motion

Untuk komponen React yang idealnya animasinya deklaratif dan terikat ke state/props React, bukan dimanipulasi manual lewat DOM.

```jsx
import { motion } from "framer-motion";

export function FadeInCard({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}
```
