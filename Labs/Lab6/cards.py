"""
Contains the class definitions for all Card Types alongside any
interfaces or supporting classes that they might use.
"""
from abc import ABC, abstractmethod
from datetime import date


class Expirable(ABC):
    """
    Describes an interface that mandates the implementation of an expiry
    date for a card. Contains a property called "expired" that validates
    the expiry date with the system clock.
    """

    def __init__(self, expiry_day, expiry_month, expiry_year, **kwargs):
        """
        Initialize an Expirable with data that describes a expiry date
        :param expiry_day: a string that represents a number from 1-31
        :param expiry_month: a string that represents a number from 1-12
        :param expiry_year: a string that represents a 4-digit year.
        :param kwargs: other named arguments to support multiple
        inheritance
        """
        self._expiry_date = date(int(expiry_year), int(expiry_month),
                                 int(expiry_day))
        super().__init__(**kwargs)

    @property
    def expired(self):
        """
        A property that calculates the expiry status of a card with
        respect to system clock.
        :return: True if the expiry date has passed, False otherwise
        """
        if date.today() >= self._expiry_date:
            return True
        return False

    @classmethod
    @abstractmethod
    def get_fields(cls):
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        fields["expiry_year"] = "Expiry Year"
        fields["expiry_month"] = "Expiry Month"
        fields["expiry_day"] = "Expiry Day"
        return fields

    def __str__(self):
        formatted_str = super().__str__()
        formatted_str = f"{formatted_str}\nExpiry Date: {self._expiry_date}"
        return formatted_str


class ContactDetails:
    """
    Represents a collection of contact details of an individual that
    owns a card.

    The class models a name, date of birth, address,
    email, and a telephone number. Of these only the name is mandatory as
    different cards will require different details. The rest are optional
    and initialize to None if not provided.
    """

    field_map = {
        "name": "Name",
        "date_of_birth": "Date of Birth",
        "address": "Address",
        "email": "E-mail",
        "tel_number": "Telephone Number"
    }
    """ 
    A dictionary to map attributes to their string representations
    """

    def __init__(self, name, date_of_birth=None, address=None, email=None,
                 tel_number=None):
        self.name = name
        self.date_of_birth = date_of_birth
        self.address = address
        self.email = email
        self.tel_number = tel_number

    def get_details(self):
        """
        :return: Returns a dictionary of the string representation
        of attributes and their value, if initialized.
        """
        details = {}
        for key, value in self.__dict__.items():
            if value:
                details[self.field_map[key]] = value
        return details


class Card(ABC):
    """
    An abstract base class that represents a class. In the event that
    this class is one of many being inherited, inherit this class last.
    By default all cards have a issuer name, and a card id.
    """

    def __init__(self, issuer_name, card_id, **kwargs):
        """
        Initializes a card.
        :param issuer_name: a string
        :param card_id: a string
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        self._issuer_name = issuer_name
        self._card_id = card_id
        super().__init__(**kwargs)

    @property
    def card_id(self):
        """
        Read only property of the _card_id attribute, which should not
        be set outside the constructor.
        :return: a string
        """
        return self._card_id

    @abstractmethod
    def validate_card(self):
        """
        Contains the logic to check if a card is valid or note. The
        exact algorithm would vary card to card.
        :return:
        """
        pass

    @classmethod
    @abstractmethod
    def get_fields(cls):
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = {
            "issuer_name": "Issuer Organization",
            "card_id": "Card ID"
        }
        return fields

    @abstractmethod
    def __str__(self):
        return f"Issuer Name: {self._issuer_name}\n" \
               f"Card ID: {self.card_id}"


class IDCard(Expirable, Card):
    """
    An ID card here refers to a card issued by the government or a
    school and has an ID that begins with the letter A followed by
    numbers.

    This class impelemnts and inherits the Expirable interface and the
    Card base class.
    """

    def __init__(self, name, dob_year, dob_month, dob_day, **kwargs):
        """
        Initializes an ID card.
        :param name: a string
        :param dob_year: a string
        :param dob_month: a string
        :param dob_day: a string
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        date_of_birth = date(int(dob_year), int(dob_month), int(dob_day))
        self.contact_details = ContactDetails(name=name,
                                              date_of_birth=date_of_birth)
        super().__init__(**kwargs)

    def validate_card(self):
        """
        Validates an ID card. An ID card is valid if it is not expired
        and has a card id folllowing the format A###### where # is a
        number.
        :return: True if valid, False otherwise
        """
        if not self.expired and self.card_id[:1] == "A" and \
                self.card_id[1:].isdigit():
            return True
        return False

    @classmethod
    def get_fields(cls):
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        fields["name"] = "Name"
        fields["dob_year"] = "Date Of Birth Year"
        fields["dob_month"] = "Date of Birth Month"
        fields["dob_day"] = "Date of Birth Day"
        return fields

    def __str__(self):
        formatted = super().__str__()
        for key, value in self.contact_details.get_details().items():
            formatted = f"{formatted}\n{key}: {value}"
        return formatted


class BalanceCard(Card, ABC):
    """
    A BalanceCard represents a card with a balance. BalanceCard is
    abstract and needs to be inherited to be instantiated.
    """

    def __init__(self, balance, **kwargs):
        """
        Initialize a BalanceCard.
        :param balance: float
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        super().__init__(**kwargs)
        self._balance = float(balance)

    def __str__(self):
        """String representation of an instance."""
        return f'Balance Card with Balance of: ' \
               f'{self._balance}, {super().__str__()}'

    @abstractmethod
    def validate_card(self):
        pass

    @classmethod
    @abstractmethod
    def get_fields(cls):
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        fields["balance"] = "Card Balance"
        return fields


class TransitCard(BalanceCard):
    """
    A Transit card Represents a transit card used for buses.
    Transit cards have a balance that must be above 0.
    """

    def __init__(self, name, email, monthly_pass, **kwargs):
        """
        Initialize a TransitCard.
        :param name: a string
        :param email: a string
        :param monthly_pass: a string 'yes' for True
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        if monthly_pass.lower() == 'yes':
            self.has_monthly_pass = True
        else:
            self.has_monthly_pass = False
        self.contact_details = ContactDetails(name=name, email=email)
        super().__init__(**kwargs)

    def validate_card(self):
        """
        To validate a TransitCard, it must have a balance ≥ 0 and
        it's card_id must begin with the letter 'T' and be followed by
        digits
        :return: bool True if valid

        """
        balance_check = self._balance >= 0
        letter_check = self.card_id[0] == 'T' and self.card_id[1:].isdigit()
        return balance_check and letter_check

    def __str__(self):
        """String representation of an instance."""
        return f'TransitCard with contact details: ' \
               f'Name: {self.contact_details.name},' \
               f' email: {self.contact_details.email} ' \
               f'Monthly pass: {self.has_monthly_pass}, Card details: ' \
               f'{super().__str__()}'

    @classmethod
    def get_fields(cls):
        """
        Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        :return: bool True if valid
        """
        fields = super().get_fields()
        fields["name"] = "Name"
        fields["email"] = "Email"
        fields["monthly_pass"] = "Has Monthly Pass"
        return fields


class GiftCard(Expirable, BalanceCard):
    """
    A GiftCard Represents a gift card used for in store purchases only.
    Gift cards have a balance that must be above 0.
    """

    def __init__(self, **kwargs):
        """
        Initialize a GiftCard.
        :param kwargs: a dictionary of named arguments and values. This
        is to provide support in the event of multiple inheritance and
        complex super() MRO calls. Usually contains the attributes of
        other interfaces that have been implemented.
        """
        super().__init__(**kwargs)

    def validate_card(self):
        """
        To validate a GiftCard it must have a balance ≥ 0, not be
        expired and have a card_id hat begins with the letter 'G' and
        be followed by digits.
        :return: bool True if valid
        """
        balance_check = self._balance >= 0
        letter_check = self.card_id[0] == 'G' and self.card_id[1:].isdigit()
        return balance_check and letter_check

    def __str__(self):
        """String representation of an instance."""
        return f'GiftCard Card details: {super().__str__()}'

    @classmethod
    def get_fields(cls):
        """
        :return: Returns a dictionary of attributes and their string
        representations to allow a Menu class to dynamically initialize
        the class using kwargs.
        """
        fields = super().get_fields()
        return fields
