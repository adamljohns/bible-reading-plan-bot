/* give.js — online giving button (Stripe Payment Links).
 *
 * One config for every page that carries a donate block. Any element with
 * [data-give-card] gets the online-giving button rendered into it. While the
 * links below are empty the slot renders nothing, so a page never shows a
 * button that goes nowhere.
 *
 * The Stripe-hosted page takes cards, Apple Pay, Google Pay and Link; which
 * wallets appear is controlled in the Stripe Dashboard (Settings → Payment
 * methods), not here. These URLs are public links, not secrets.
 */
(function () {
  "use strict";

  var GIVE = {
    // "Customers choose what to pay" Payment Link — one-time gift, any amount.
    oneTime: "",
    // Optional fixed-amount monthly links. Choose-your-amount links cannot recur.
    monthly: [
      // { amount: 25, url: "" },
      // { amount: 50, url: "" },
      // { amount: 100, url: "" }
    ]
  };

  var ALLOWED_HOSTS = ["buy.stripe.com", "donate.stripe.com"];

  function safeUrl(raw) {
    if (!raw) return null;
    try {
      var u = new URL(raw);
      if (u.protocol !== "https:" || ALLOWED_HOSTS.indexOf(u.hostname) === -1) return null;
      // Lets Stripe reporting show which page a gift came from.
      var page = (location.pathname.split("/").pop() || "index.html").replace(/\.html$/, "");
      u.searchParams.set("utm_source", "usmcmin.org");
      u.searchParams.set("utm_content", page);
      return u.toString();
    } catch (e) {
      return null;
    }
  }

  function el(tag, style, text) {
    var n = document.createElement(tag);
    if (style) n.setAttribute("style", style);
    if (text) n.textContent = text;
    return n;
  }

  function link(href, label, style) {
    var a = el("a", style, label);
    a.href = href;
    a.target = "_blank";
    a.rel = "noopener";
    return a;
  }

  function render(slot) {
    var one = safeUrl(GIVE.oneTime);
    var monthly = (GIVE.monthly || [])
      .map(function (m) { return { amount: m.amount, url: safeUrl(m.url) }; })
      .filter(function (m) { return m.url && m.amount > 0; });
    if (!one && !monthly.length) return;

    var wrap = el("div", "text-align:center;margin:0 auto 28px;max-width:520px;");

    if (one) {
      wrap.appendChild(link(one, "Give online",
        "display:inline-block;padding:16px 36px;background:var(--gold,#D4AF37);color:#14181f;" +
        "border-radius:12px;font-weight:700;font-size:1.08rem;text-decoration:none;"));
      wrap.appendChild(el("div",
        "color:var(--gray,#9aa3ad);font-size:0.85rem;margin-top:10px;",
        "Card · Apple Pay · Google Pay · Link — secure checkout by Stripe"));
    }

    if (monthly.length) {
      var row = el("div", "display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-top:16px;");
      monthly.forEach(function (m) {
        row.appendChild(link(m.url, "$" + m.amount + " / month",
          "display:inline-block;padding:10px 18px;border:1px solid var(--gold,#D4AF37);" +
          "color:var(--gold,#D4AF37);border-radius:10px;font-weight:600;font-size:0.95rem;text-decoration:none;"));
      });
      wrap.appendChild(el("div",
        "color:var(--gray,#9aa3ad);font-size:0.85rem;margin-top:18px;", "Or stand with us monthly"));
      wrap.appendChild(row);
    }

    slot.appendChild(wrap);
    slot.hidden = false;
  }

  function init() {
    var slots = document.querySelectorAll("[data-give-card]");
    for (var i = 0; i < slots.length; i++) render(slots[i]);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
