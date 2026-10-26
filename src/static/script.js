document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const feedback = document.getElementById('feedback');

    feedback.textContent = 'Aguarde...';
    feedback.className = '';

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            feedback.textContent = 'Login aprovado!';
            feedback.className = 'success';
        } else if (response.status === 401) {
            feedback.textContent = 'Credenciais incorretas.';
            feedback.className = 'error';
        } else {
            feedback.textContent = 'Erro no servidor.';
            feedback.className = 'error';
        }
    } catch (error) {
        feedback.textContent = 'Falha na conexão.';
        feedback.className = 'error';
    }
});