# import typing

from pathlib import Path

from json import (
    loads as json_loads,
    dumps as json_dumps,
    decoder as json_decoder
)

from socket import(
    inet_aton as socket_inet_aton,
    inet_ntoa as socket_inet_ntoa
)

from struct import(
    pack as struct_pack,
    unpack as struct_unpack,
)

from random import (
    randint as r_randint,
    choice as r_choice,
    seed as r_seed
)


from . import exceptions as ex


class RandomIp4:

    ip_list: list = []
    """The list of created IPs to prevent the creation of duplicate IPs
        ----
    """

    def __init__(self, country_code: set = "ALL", random_seed=None) -> None:
        """To generate random IP
            ----
            - Args:
                - country_code (set, optional): Enter the country code or you can enter "all" instead of the country code. In this case, the generated IP can be for any country . Defaults to "ALL".
                - random_seed (str or int, optional): used to initialize the random ip generator . Defaults to None.

            - ip_list : The created IPs are added to the ip_list list to prevent the creation of duplicate IPs
        """

        self.random_seed = random_seed
        """random seed
            ---- 
        """

        self.country_code: str = country_code.upper()
        """country code
            ---- 
        """

        data_file_location = Path(__file__).resolve().parent / "data.json"


        try:
            with open(data_file_location, "r", encoding="utf8") as file:
                self.data: dict = json_loads(file.read())

        except json_decoder.JSONDecodeError as err:
            raise ex.ReadDataFileError(
                f"Error in {data_file_location} file \n\t Error in JSON file "
            )

        except FileNotFoundError as err:
            raise ex.DataFileNotFoundError(
                f"Error in {data_file_location} file \n\t[Data File Not Found ]"
            )

        if self.country_code not in self.data.keys() and self.country_code != "ALL":
            raise ex.CountryCodeNotFoundError(
                f"Error : The country code ({self.country_code}) was not found in the data file"
            )

        self.country_data = dict(
            country_code=self.country_code,
            country_name="All countries" if self.country_code == "ALL" else self.data.get(self.country_code),
            ranges=sum(list(map(lambda c_code: self.data.get(c_code).get("ranges"), list(self.data.keys()))), [])
        ) if self.country_code == "ALL" else self.data.get(self.country_code)
        """Country data
            ----
        """

        self.country_ranges = list(
            zip(
                list(map(lambda dict_: (dict_.get("begin_ip"), dict_.get("end_ip")), self.country_data.get("ranges"))),
                list(map(lambda dict_: (struct_unpack('>I', socket_inet_aton(dict_["begin_ip"]))[0], struct_unpack('>I', socket_inet_aton(dict_["end_ip"]))[0]), self.country_data.get('ranges')))
            )
        )
        """ ip ranges of countries 
            ---
            ______________
            
            Structure:
            
                - list
                    - tuple
                        - index: 0 : ip ranges of country
                            - index: 0 : begin_ip
                            - index: 1 : end_ip
                        - index: 1 : unpacked ip ranges of country
                            - index: 0 : begin_ip
                            - index: 1 : end_ip
                    - tuple ...
                    - tuple ...
                    - tuple ...
        """

        self.country_name = self.country_data.get("country_name")
        """country name
            ---- 
        """

    def generate_ip(self):
        """generate ip
        ----
        #### Use `generate_ip` to generate an IP. It will return the created IP to you and add it to the `ip_list` list
        
        - Returns:
            - str: ip v4
        """
        if bool(self.random_seed):
            r_seed(self.random_seed)

        while True:
            range_ = r_choice(self.country_ranges)[1]
            ip = socket_inet_ntoa(struct_pack('>I', r_randint(range_[0], range_[1])))

            if ip not in self.ip_list:
                self.ip_list.append(ip)
                break
        self.ip = ip

        return ip

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ip_list.clear()
        del(self.country_data)
        del(self.country_ranges)
        del(self.data)
        del(self.country_name)
        del(self.country_code)
