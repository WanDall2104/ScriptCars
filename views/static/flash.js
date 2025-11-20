document.addEventListener('DOMContentLoaded', () => {
    const DISMISS_MS = 5000; // tempo em ms até começar a sumir
    const FADE_DURATION = 300; // duração do fade em ms

    const alerts = document.querySelectorAll('.flash-messages .alert, .alert');
    if (!alerts || alerts.length === 0) return;

    alerts.forEach(alert => {
        // garante que a transição exista
        alert.style.transition = `opacity ${FADE_DURATION}ms ease`;
        // remove após o tempo configurado
        setTimeout(() => {
            alert.style.opacity = '0';
            // remove do DOM depois do fade
            setTimeout(() => {
                if (alert.parentNode) alert.parentNode.removeChild(alert);
            }, FADE_DURATION);
        }, DISMISS_MS);
    });
});
