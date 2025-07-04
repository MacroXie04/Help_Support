/** Bootstrap‑friendly live deadline countdown. */
(function () {
    "use strict";
    const el = document.getElementById("countdown");
    if (!el || !el.dataset.deadline) {
        if (el) el.textContent = "N/A";
        return;
    }
    const deadline = Date.parse(el.dataset.deadline);
    const interval = setInterval(tick, 1000);

    function pad(n) {
        return n.toString().padStart(2, "0");
    }

    function tick() {
        const diff = deadline - Date.now();
        if (diff <= 0) {
            el.textContent = "Expired";
            clearInterval(interval);
            return;
        }
        const s = Math.floor(diff / 1000) % 60;
        const m = Math.floor(diff / 60000) % 60;
        const h = Math.floor(diff / 3600000) % 24;
        const d = Math.floor(diff / 86400000);
        el.textContent = (d ? d + "d " : "") + pad(h) + ":" + pad(m) + ":" + pad(s);
    }

    tick();
})();