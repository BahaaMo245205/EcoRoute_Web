function togglePassword(buttonId, passwordIds) {
    const btn = document.getElementById(buttonId);
    if (!btn) return;

    btn.addEventListener('click', () => {
        passwordIds.forEach(id => {
            const input = document.getElementById(id);
            if (input) {
                input.type = input.type === 'password' ? 'text' : 'password';
            }
        });
    });
}

togglePassword('ShowPassword-signup', ['password-signup', 'confirmPassword']);
togglePassword('ShowPassword-login', ['password-login']);
togglePassword('ShowPassword-user', ['old-password','password-user', 'confirm-password-user']);
togglePassword('ShowPassword-reset', ['password-reset', 'confirm-password-reset']);