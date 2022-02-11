// Scrolling Effect
const header = document.querySelector(".navbar");
const sectionOne = document.querySelector(".hero-container");
const overlay = document.querySelector(".hero-overlay");

// const swiper = new Swiper(".swiper", {
//   // Optional parameters
//   direction: "vertical",
//   loop: true,

//   // If we need pagination
//   pagination: {
//     el: ".swiper-pagination",
//   },

//   // Navigation arrows
//   navigation: {
//     nextEl: ".swiper-button-next",
//     prevEl: ".swiper-button-prev",
//   },
// });

function change(x) {
  x.classList.toggle("animate");
  AOS.init();
}
/**
 * Easy selector helper function
 */
const select = (el, all = false) => {
  el = el.trim();
  if (all) {
    return [...document.querySelectorAll(el)];
  } else {
    return document.querySelector(el);
  }
};

/**
 * Easy event listener function
 */
const on = (type, el, listener, all = false) => {
  let selectEl = select(el, all);
  if (selectEl) {
    if (all) {
      selectEl.forEach((e) => e.addEventListener(type, listener));
    } else {
      selectEl.addEventListener(type, listener);
    }
  }
};

/**
 * Easy on scroll event listener
 */
const onscroll = (el, listener) => {
  el.addEventListener("scroll", listener);
};

/**
 * Navbar links active state on scroll
 */
let navbarlinks = select("#navbar .scrollto", true);
const navbarlinksActive = () => {
  let position = window.scrollY + 200;
  navbarlinks.forEach((navbarlink) => {
    if (!navbarlink.hash) return;
    let section = select(navbarlink.hash);
    if (!section) return;
    if (
      position >= section.offsetTop &&
      position <= section.offsetTop + section.offsetHeight
    ) {
      navbarlink.classList.add("active");
    } else {
      navbarlink.classList.remove("active");
    }
  });
};
window.addEventListener("load", navbarlinksActive);
onscroll(document, navbarlinksActive);

/**
 * Toggle .header-scrolled class to #header when page is scrolled
 */
// let selectHeader = select("#header");
// if (selectHeader) {
//   const headerScrolled = () => {
//     if (window.scrollY > 100) {
//       selectHeader.classList.add("header-scrolled");
//     } else {
//       selectHeader.classList.remove("header-scrolled");
//     }
//   };
//   window.addEventListener("load", headerScrolled);
//   onscroll(document, headerScrolled);
// }

/**
 * Back to top button
 */
let backtotop = select(".back-to-top");
if (backtotop) {
  const toggleBacktotop = () => {
    if (window.scrollY > 100) {
      backtotop.classList.add("active");
    } else {
      backtotop.classList.remove("active");
    }
  };
  window.addEventListener("load", toggleBacktotop);
  onscroll(document, toggleBacktotop);
}

/**
 * Scrolls to an element with header offset
 */
// const scrollto = (el) => {
//   let header = select("#header");
//   let offset = header.offsetHeight;

//   if (!header.classList.contains("header-scrolled")) {
//     offset -= 24;
//   }

//   let elementPos = select(el).offsetTop;
//   window.scrollTo({
//     top: elementPos - offset,
//     behavior: "smooth",
//   });
// };

const sectionOneOptions = {
  rootMargin: "-810px 0px 0px 0px",
};

const sectionOneObserver = new IntersectionObserver(function (
  entries,
  sectionOneObserver
) {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) {
      header.classList.add("nav-scrolled");
      overlay.classList.remove("overlay");
    } else {
      header.classList.remove("nav-scrolled");
      overlay.classList.add("overlay");
    }
  });
},
sectionOneOptions);

sectionOneObserver.observe(sectionOne);

/**
 * Porfolio isotope and filter
 */
window.addEventListener("load", () => {
  let portfolioContainer = select(".portfolio-container");
  if (portfolioContainer) {
    let portfolioIsotope = new Isotope(portfolioContainer, {
      itemSelector: ".portfolio-item",
      layoutMode: "fitRows",
    });

    let portfolioFilters = select("#portfolio-flters li", true);

    on(
      "click",
      "#portfolio-flters li",
      function (e) {
        e.preventDefault();
        portfolioFilters.forEach(function (el) {
          el.classList.remove("filter-active");
        });
        this.classList.add("filter-active");

        portfolioIsotope.arrange({
          filter: this.getAttribute("data-filter"),
        });
        aos_init();
      },
      true
    );
  }
});

/**
 * Initiate portfolio lightbox
 */
const portfolioLightbox = GLightbox({
  selector: ".portfokio-lightbox",
});
const glightbox = GLightbox({
  openEffect: "zoom",
  closeEffect: "fade",
  cssEfects: {
    // This are some of the animations included, no need to overwrite
    fade: { in: "fadeIn", out: "fadeOut" },
    zoom: { in: "zoomIn", out: "zoomOut" },
  },
});
