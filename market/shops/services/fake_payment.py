
class PaymentError(Exception):
    """Исключение, возникающее при ошибке обработки платежа"""
    pass


class FakePaymentService:
    """cервис фиктивной оплаты, который будет имитировать внешний сервис оплаты"""
    def pay_order(self, card_number):
        if card_number % 2 == 0 and str(card_number[-1]) != '0' and len(str(card_number)) == 8:
            return 'success'
        elif card_number % 2 != 0 and str(card_number[-1]) == '0' and len(str(card_number)) != 8:
            raise PaymentError('Payment error')
        else:
            return 'error'
