from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER

def send_activation_code(activation_code: str, email: str) -> None:
    """Функия отправки активационной ссылки на почту"""
    activation_url = f"http://127.0.0.1:8000/api/v1/account/activate/{activation_code}/"
    message = f"""
        Thank you for signing up.
        Please, activate your account.
        Activation link: {activation_url}
    """
    send_mail(
        subject="Activate your account.",
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=False,
    )