#!/usr/bin/env python3

# > Importing modules

import requests
import requests_cache
from bs4 import BeautifulSoup
import pandas as pd
from erros import XchangerException
import os
import tqdm
from termcolor import colored
import itertools
import threading
import sys
import time


class Xchanger:
    """
    This module enables us to scrap data from https://www.xe.com/ and returns rate excahnge between different currencies.

    Parameters
    ----------
    amount : str, optional
        The amount parameter is the amount of the currency to be exchanged.
        The amount parameter is optional and defaults to 1.

    from_currency: str, optional
        The from_currency parameter is the currency being exchanged.

    to_currency: str, optional
        The to_currency parameter is the currency being exchanged to.

    proxies: str, optional
        The proxies parameter is a string that represents the proxy to use when making requests to the XE API.

    Returns
    -------
    out 1: Returns the exchange rate between two currencies.
    out 2: Returns a file of all the currencies exchange rate of a specific currency.

    Note:
    ----
        This module may create a file named url_cache.sqlite to store the cache of the requests.
        The cache will expire after 1 hour (3600 seconds).
        To clear the cache, you can delete the `url_cache.sqlite` file (NOT RECOMMENDED).

    """

    def __init__(self, amount=1, from_currency="USD", to_currency="PKR", proxies=None):
        self.amount = amount
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.proxies = proxies
        self.url = (
            "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=PKR"
        )
        self._animation_done = False
        self.only_supported_currencies = [
            "USD",
            "EUR",
            "GBP",
            "CAD",
            "AUD",
            "JPY",
            "INR",
            "NZD",
            "CHF",
            "ZAR",
            "RUB",
            "BGN",
            "SGD",
            "HKD",
            "SEK",
            "THB",
            "HUF",
            "CNY",
            "NOK",
            "MXN",
            "DKK",
            "MYR",
            "PLN",
            "BRL",
            "PHP",
            "IDR",
            "CZK",
            "AED",
            "TWD",
            "KRW",
            "ILS",
            "ARS",
            "CLP",
            "EGP",
            "TRY",
            "RON",
            "SAR",
            "PKR",
            "COP",
            "IQD",
            "XAU",
            "FJD",
            "KWD",
            "BAM",
            "ISK",
            "MAD",
            "HRK",
            "VND",
            "JMD",
            "JOD",
            "DOP",
            "PEN",
            "CRC",
            "BHD",
            "BDT",
            "DZD",
            "KES",
            "XAG",
            "LKR",
            "OMR",
            "QAR",
            "XOF",
            "IRR",
            "XCD",
            "TND",
            "TTD",
            "XPF",
            "EEK",
            "ZMK",
            "ZMW",
            "BBD",
            "NGN",
            "LBP",
            "XAF",
            "MUR",
            "XPT",
            "BSD",
            "ALL",
            "UYU",
            "BMD",
            "LVL",
            "UAH",
            "GTQ",
            "XDR",
            "BWP",
            "BOB",
            "CUP",
            "PYG",
            "HNL",
            "LTL",
            "ZWD",
            "NIO",
            "RSD",
            "NPR",
            "HTG",
            "PAB",
            "SVC",
            "GYD",
            "KYD",
            "TZS",
            "CNH",
            "CVE",
            "FKP",
            "ANG",
            "UGX",
            "MGA",
            "GEL",
            "ETB",
            "MDL",
            "VUV",
            "SYP",
            "BND",
            "KHR",
            "NAD",
            "MKD",
            "AOA",
            "PGK",
            "MMK",
            "KZT",
            "MOP",
            "MZN",
            "LYD",
            "SLE",
            "SLL",
            "GNF",
            "BYN",
            "BYR",
            "GMD",
            "AWG",
            "AMD",
            "YER",
            "LAK",
            "WST",
            "MWK",
            "KPW",
            "BIF",
            "DJF",
            "MNT",
            "UZS",
            "TOP",
            "SCR",
            "KGS",
            "BTN",
            "SBD",
            "GIP",
            "RWF",
            "CDF",
            "MVR",
            "MRU",
            "ERN",
            "SOS",
            "SZL",
            "TJS",
            "LRD",
            "LSL",
            "SHP",
            "STN",
            "KMF",
            "SPL",
            "TMT",
            "SRD",
            "IMP",
            "JEP",
            "TVD",
            "GGP",
            "AFN",
            "AZN",
            "BZD",
            "CUC",
            "GHS",
            "SDG",
            "VES",
            "VEF",
            "XPD",
            "BTC",
            "ADA",
            "BCH",
            "DOGE",
            "DOT",
            "ETH",
            "LINK",
            "LTC",
            "LUNA",
            "UNI" "",
            "XLM",
            "XRP",
            "ATS",
            "AZM",
            "BEF",
            "CYP",
            "DEM",
            "ESP",
            "FIM",
            "FRF",
            "GHC",
            "GRD",
            "IEP",
            "ITL",
            "LUF",
            "MGF",
            "MRO",
            "MTL",
            "MZM",
            "NLG",
            "PTE",
            "ROL",
            "SDD",
            "SIT",
            "SKK",
            "SRG",
            "STD",
            "TMM",
            "TRL",
            "VAL",
            "VEB",
            "XEU",
        ]

    def _is_proxy(self, proxies):
        "Checks if the class proxy attribute is None or not."
        if proxies != None:
            return True
        else:
            return False

    def _check_proxies(self, proxies, get_name=False):
        "Checks is the proxy works or not"
        if self._is_proxy(proxies):
            try:
                responce = requests.get(
                    "https://api.ipify.org?format=json", proxies=proxies
                )
                if responce.status_code == 200:
                    if get_name:
                        message = f"Your Public IP Address is {responce.text}"
                        return [True, message]
                    else:
                        return True
                else:
                    raise XchangerException(
                        f"Your Proxy is not wroking! Status code : {responce.status_code}"
                    )
            except Exception as e:
                raise XchangerException(f"Fail to check the proxy. Error : {e}")

    def _making_url(self):
        "Get the URL of the given currencies."
        if (
            self.amount == 1
            and self.from_currency == "USD"
            and self.to_currency == "PKR"
        ):
            new_url = self.url

        else:
            new_url = f"https://www.xe.com/currencyconverter/convert/?Amount={self.amount}&From={self.from_currency}&To={self.to_currency}"

        return new_url

    def _animation(self):
        "Create a simple animation"
        for char in itertools.cycle(["| ", "/ ", "- ", "\\ "]):
            if self._animation_done:
                break
            sys.stdout.write(
                colored(
                    "\rloading ",
                    "green",
                )
                + colored(char, "green")
            )
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write(colored("\rDone!     ", "blue"))

    def _making_requests(self):
        "Make requests to scrap data"
        self.url = self._making_url()
        try:
            if self._check_proxies(self.proxies):
                responce = requests.get(self.url, self.proxies)
            else:
                responce = requests.get(self.url)
            if responce.status_code == 200:
                return responce
            else:
                raise XchangerException(
                    f"Access denied. Status Code : {responce.status_code}"
                )
        except Exception as e:
            raise XchangerException(
                f"The data you provided is incorrect. The only currencies supported by this module are: {self.only_supported_currencies}"
            )

    def _get_data(self):
        "Scrapping data from different currencies"
        responce = self._making_requests()
        try:
            main_soup = BeautifulSoup(responce.text, "lxml")
            xchange_rate_to_2_from = main_soup.find(
                "p", class_="result__BigRate-sc-1bsijpp-1 iGrAod"
            ).text.split(" ")[0]
            return xchange_rate_to_2_from

        except Exception as e:
            raise XchangerException(f"Fail to make the soup. Error : {e}")

    def get(self, amount=1, from_currency="USD", to_currency="PKR", proxies=None):
        "Returns the data of the specified currencies."
        self.amount = amount
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.proxies = proxies
        try:
            print(colored("\nStarting Xchanger...", "green"))
            t = threading.Thread(target=self._animation, daemon=True)
            t.start()
            rate = self._get_data()
            rate_text = (
                f"{self.amount} {self.from_currency} = {rate} {self.to_currency}"
            )
            self._animation_done = True
            time.sleep(0.8)
            print("\n")
            return colored(rate_text, "blue")
        except Exception as e:
            raise XchangerException(f"Fail to get data. Error : {e}")

    def _get_data_urls(self, amount, from_currency, to_currency):
        "Get data from the different URLs of the currencies."
        if (
            from_currency != None
            and from_currency not in self.only_supported_currencies
        ):
            raise XchangerException(
                f"The data you provided is incorrect. The only currencies supported by this module are: {self.only_supported_currencies}"
            )

        if to_currency != None and to_currency not in self.only_supported_currencies:
            raise XchangerException(
                f"The data you provided is incorrect. The only currencies supported by this module are: {self.only_supported_currencies}"
            )

        else:
            if (from_currency != None and to_currency == None) or (
                from_currency == None and to_currency != None
            ):
                url_list = self._making_url_list(amount, from_currency, to_currency)
                responce_url_list = self._making_requests_urls(url_list)
                data = self._data_urls(responce_url_list)
                return data

            else:
                raise XchangerException(
                    "Specify one currency at a time. If only one currency is given, the other currency must be None."
                )

    def _making_url_list(
        self, amount: int, from_currency: str, to_currency: str | None
    ):
        "Create a list of the different URLs of the currencies."
        url_list = []
        for country_code in self.only_supported_currencies:
            if from_currency == None:
                try:
                    new_url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={country_code}&To={to_currency}"
                    url_list.append(new_url)
                except Exception as e:
                    raise XchangerException(
                        f"Fail to load the link {new_url}. Error : {e}"
                    )

            elif to_currency == None:
                try:
                    new_url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_currency}&To={country_code}"
                    url_list.append(new_url)
                except Exception as e:
                    raise XchangerException(
                        f"Fail to load the link {new_url}. Error : {e}"
                    )
        return url_list

    def _making_requests_urls(self, url_list: list):
        "Make requests to the different URLs to scrape data"
        responce_url_list = []
        module_dir = os.path.dirname(os.path.abspath(__file__))
        cache_file_path = os.path.join(module_dir, "url_cache.sqlite")
        requests_cache.install_cache(cache_file_path, expire_after=3600)
        print("")
        with tqdm.tqdm(
            total=len(url_list), desc="Fetching URLs", colour="green"
        ) as pbar:  # simple animation
            for url in url_list:
                try:
                    if self._check_proxies(self.proxies):
                        responce = requests.get(url, self.proxies)
                        pbar.update(1)
                    else:
                        responce = requests.get(url)
                        pbar.update(1)
                    if responce.status_code == 200:
                        responce_url_list.append(responce.text)
                    else:
                        responce_url_list.append("None")

                except Exception as e:
                    raise XchangerException(
                        f"The data you provided is incorrect. The only currencies supported by this module are: {self.only_supported_currencies}. Error : {e} from {url}"
                    )
        return responce_url_list

    def _data_urls(self, responce_url_list):
        "Scrape data from the different URLs."
        data_list = []
        print("")
        with tqdm.tqdm(
            total=len(responce_url_list), desc="scraping data", colour="green"
        ) as pbar:
            for responce in responce_url_list:
                try:
                    url_soup = BeautifulSoup(responce, "lxml")
                    data_p = url_soup.find(
                        "p", class_="result__BigRate-sc-1bsijpp-1 iGrAod"
                    )
                    if data_p != None:
                        xchange_rate = data_p.text.split(" ")[0]
                        data_list.append(xchange_rate)
                        pbar.update(1)
                    else:
                        data_list.append("None")
                        pbar.update(1)
                except Exception as e:
                    raise XchangerException(f"Fail to get data. Error : {e}.")
        return data_list

    def _making_dataframe(self, amount, from_currency, to_currency):
        """
        Makes a Pandas DataFrame of the exchange rate data.

        Args:
            amount: The amount of money to be converted.
            from_currency: The currency that the amount is in.
            to_currency: The currency that the amount is to be converted to.

        Returns:
            A Pandas DataFrame of the exchange rate data.
        """
        data = self._get_data_urls(amount, from_currency, to_currency)
        try:
            data_df = {
                "Currency": [currency for currency in self.only_supported_currencies],
                "Rate": [val for val in data],
            }
            df = pd.DataFrame(data_df)
            return df
        except Exception as e:
            raise XchangerException(f"Fail to make dataframe. Error : {e}")

    def save_to_excel(self, amount=1, from_currency="USD", to_currency=None):
        """
        Save the exchange rate data to an Excel spreadsheet.

        Args:
            amount: The amount of money to be converted.
            from_currency: The currency that the amount is in.
            to_currency: The currency that the amount is to be converted to.
        """
        print(colored("\nStarting Xchanger...", "green"))
        df = self._making_dataframe(amount, from_currency, to_currency)
        if from_currency != None:
            name_of_file = f"{amount} {from_currency} data.xlsx"
        if to_currency != None:
            name_of_file = f"{amount} {to_currency} data.xlsx"
        name = self._rename_filename(name_of_file)
        df.to_excel(f"{name}", "Currency Data")
        print("")
        last_msg = colored(f"{name} saved succcessfully!", "blue")
        print(last_msg)
        return

    def save_to_csv(self, amount=1, from_currency="USD", to_currency=None):
        """
        Save the exchange rate data to a CSV file.

        Args:
            amount: The amount of money to be converted.
            from_currency: The currency that the amount is in.
            to_currency: The currency that the amount is to be converted to.
        """
        print(colored("\nStarting Xchanger...", "green"))
        df = self._making_dataframe(amount, from_currency, to_currency)
        if from_currency != None:
            name_of_file = f"{amount} {from_currency} data.csv"
        if to_currency != None:
            name_of_file = f"{amount} {to_currency} data.csv"
        name = self._rename_filename(name_of_file)
        df.to_csv(f"{name}")
        print("")
        last_msg = colored(f"{name} saved succcessfully!", "blue")
        print(last_msg)
        return

    def save_to_json(self, amount=1, from_currency="USD", to_currency=None):
        """
        Save the exchange rate data to a JSON file.

        Args:
            amount: The amount of money to be converted.
            from_currency: The currency that the amount is in.
            to_currency: The currency that the amount is to be converted to.
        """
        print(colored("\nStarting Xchanger...", "green"))
        df = self._making_dataframe(amount, from_currency, to_currency)
        if from_currency != None:
            name_of_file = f"{amount} {from_currency} data.json"
        if to_currency != None:
            name_of_file = f"{amount} {to_currency} data.json"
        name = self._rename_filename(name_of_file)
        df.to_json(f"{name}", orient="records")
        print("")
        last_msg = colored(f"{name} saved succcessfully!", "blue")
        print(last_msg)
        return

    def _rename_filename(self, name_of_file):
        """
        Renames a file if the file name already exists.

        Args:
            name_of_file: The name of the file to be renamed.

        Returns:
            The renamed file name.
        """
        name = name_of_file
        for i in range(1, 1000):
            if name_of_file in os.listdir():
                name_of_file = name
                name_of_file = name_of_file.split(".")
                name_of_file = f"{name_of_file[0]}{i}.{name_of_file[1]}"
            else:
                return name_of_file


# !    |--------------------------------- The END --------------------------------------|
