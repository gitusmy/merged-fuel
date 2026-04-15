#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime

URLS = {
    "america": "https://raw.githubusercontent.com/gitusmy/fuel-prices/refs/heads/main/tolls_fuel_prices_america.json",
    "asia": "https://raw.githubusercontent.com/gitusmy/fuel-prices/refs/heads/main/tolls_fuel_prices_asia.json",
    "europe": "https://raw.githubusercontent.com/gitusmy/fuel-prices/refs/heads/main/tolls_fuel_prices_europe.json",
    "gasoline": "https://raw.githubusercontent.com/gitusmy/fuel-prices/refs/heads/main/gasoline_prices.json",
    "fuel": "https://raw.githubusercontent.com/gitusmy/fuel-prices/refs/heads/main/fuel_prices.json",
    "currency_rates": "https://raw.githubusercontent.com/gitusmy/fuel-prices/refs/heads/main/currency_rates.json",
}

CURRENCY_SYMBOLS = {
    "Germany": "€", "France": "€", "Italy": "€", "Spain": "€", "Netherlands": "€",
    "Belgium": "€", "Austria": "€", "Portugal": "€", "Ireland": "€", "Finland": "€",
    "Greece": "€", "Slovenia": "€", "Croatia": "€", "Slovakia": "€", "Luxembourg": "€",
    "Estonia": "€", "Latvia": "€", "Lithuania": "€", "Cyprus": "€", "Malta": "€",
    "Andorra": "€", "Monaco": "€", "San Marino": "€", "Montenegro": "€", "Netherlands": "€",
    "United Kingdom": "£", "Poland": "zł", "Czechia": "Kč", "Hungary": "Ft",
    "Romania": "lei", "Bulgaria": "лв.", "Sweden": "kr", "Denmark": "kr.",
    "Norway": "kr", "Iceland": "kr", "Switzerland": "CHF", "Albania": "Lek",
    "Serbia": "din", "Turkey": "₺", "Ukraine": "₴", "Russia": "₽", "Belarus": "Br",
    "Georgia": "₾", "Moldova": "lei", "Bosnia and Herzegovina": "KM",
    "North Macedonia": "den", "Liechtenstein": "CHF", "United States": "$",
    "Canada": "C$", "Mexico": "MX$", "Brazil": "R$", "Argentina": "$",
    "Chile": "$", "Colombia": "$", "Peru": "S/.", "Uruguay": "U$",
    "Venezuela": "Bs", "Ecuador": "$", "El Salvador": "$", "Costa Rica": "₡",
    "Guatemala": "Q", "Honduras": "L", "Nicaragua": "C$", "Panama": "B.",
    "Paraguay": "₲", "Dominican Republic": "RD$", "Jamaica": "J$",
    "Trinidad And Tobago": "TT$", "Barbados": "B$", "Bahamas": "B$",
    "Belize": "BZ$", "Guyana": "G$", "Suriname": "Sr$", "Haiti": "G",
    "Puerto Rico": "$", "Cuba": "₱", "Cayman Islands": "CI$",
    "Curaçao": "ƒ", "Aruba": "ƒ", "Dominica": "EC$", "Grenada": "EC$",
    "Saint Lucia": "EC$", "Bolivia": "$b", "Japan": "¥", "China": "元",
    "South Korea": "₩", "India": "₹", "Indonesia": "Rp", "Thailand": "฿",
    "Vietnam": "₫", "Philippines": "₱", "Malaysia": "RM", "Singapore": "S$",
    "Hong Kong": "HK$", "Taiwan": "NT$", "Pakistan": "₨", "Bangladesh": "৳",
    "Sri Lanka": "₨", "Nepal": "Rs.", "Myanmar": "K", "Cambodia": "៛",
    "Laos": "₭", "Kazakhstan": "₸", "Uzbekistan": "лв", "Kyrgyzstan": "сом",
    "Armenia": "֏", "Azerbaijan": "₼", "Turkmenistan": "T", "Mongolia": "₮",
    "Afghanistan": "؋", "Iran": "﷼", "Iraq": "د.ع", "Israel": "₪",
    "Jordan": "د.أ", "Lebanon": "LL", "Syria": "£S", "Kuwait": "KD",
    "Saudi Arabia": "SAR", "Qatar": "QR", "Bahrain": "د.ب", "Oman": "﷼",
    "United Arab Emirates": "AED", "Yemen": "﷼", "Maldives": "Rf",
    "Bhutan": "Nu.", "Australia": "A$", "New Zealand": "NZ$",
}

COUNTRY_TO_CURRENCY = {
    "EUR": "EUR",
    "United Kingdom": "GBP", "Poland": "PLN", "Czechia": "CZK", "Hungary": "HUF",
    "Romania": "RON", "Bulgaria": "BGN", "Sweden": "SEK", "Denmark": "DKK",
    "Norway": "NOK", "Iceland": "ISK", "Switzerland": "CHF", "Albania": "ALL",
    "Serbia": "RSD", "Turkey": "TRY", "Ukraine": "UAH", "Russia": "RUB",
    "Belarus": "BYN", "Georgia": "GEL", "Moldova": "MDL", "Bosnia and Herzegovina": "BAM",
    "North Macedonia": "MKD", "Liechtenstein": "CHF", "United States": "USD",
    "Canada": "CAD", "Mexico": "MXN", "Brazil": "BRL", "Argentina": "ARS",
    "Chile": "CLP", "Colombia": "COP", "Peru": "PEN", "Uruguay": "UYU",
    "Venezuela": "VES", "Ecuador": "USD", "El Salvador": "USD", "Costa Rica": "CRC",
    "Guatemala": "GTQ", "Honduras": "HNL", "Nicaragua": "NIO", "Panama": "PAB",
    "Paraguay": "PYG", "Dominican Republic": "DOP", "Jamaica": "JMD",
    "Trinidad And Tobago": "TTD", "Barbados": "BBD", "Bahamas": "BSD",
    "Belize": "BZD", "Guyana": "GYD", "Suriname": "SRD", "Haiti": "HTG",
    "Puerto Rico": "USD", "Cuba": "CUP", "Cayman Islands": "KYD",
    "Curaçao": "ANG", "Aruba": "AWG", "Dominica": "XCD", "Grenada": "XCD",
    "Saint Lucia": "XCD", "Bolivia": "BOB", "Japan": "JPY", "China": "CNY",
    "South Korea": "KRW", "India": "INR", "Indonesia": "IDR", "Thailand": "THB",
    "Vietnam": "VND", "Philippines": "PHP", "Malaysia": "MYR", "Singapore": "SGD",
    "Hong Kong": "HKD", "Taiwan": "TWD", "Pakistan": "PKR", "Bangladesh": "BDT",
    "Sri Lanka": "LKR", "Nepal": "NPR", "Myanmar": "MMK", "Cambodia": "KHR",
    "Laos": "LAK", "Kazakhstan": "KZT", "Uzbekistan": "UZS", "Kyrgyzstan": "KGS",
    "Armenia": "AMD", "Azerbaijan": "AZN", "Turkmenistan": "TMT", "Mongolia": "MNT",
    "Afghanistan": "AFN", "Iran": "IRR", "Iraq": "IQD", "Israel": "ILS",
    "Jordan": "JOD", "Lebanon": "LBP", "Syria": "SYP", "Kuwait": "KWD",
    "Saudi Arabia": "SAR", "Qatar": "QAR", "Bahrain": "BHD", "Oman": "OMR",
    "United Arab Emirates": "AED", "Maldives": "MVR", "Bhutan": "INR",
    "Australia": "AUD", "New Zealand": "NZD", "Nigeria": "NGN", "South Africa": "ZAR",
    "Egypt": "EGP", "Morocco": "MAD", "Algeria": "DZD", "Tunisia": "TND",
    "Kenya": "KES", "Ghana": "GHS", "Tanzania": "TZS", "Ethiopia": "ETB",
    "Sudan": "SDG", "Zimbabwe": "ZWG", "Zambia": "ZMW", "Botswana": "BWP",
    "Namibia": "NAD", "Rwanda": "RWF", "Uganda": "UGX", "Mozambique": "MZN",
}

COUNTRY_CODE = {
    "Germany": "DE", "France": "FR", "Italy": "IT", "Spain": "ES", "Netherlands": "NL",
    "Belgium": "BE", "Austria": "AT", "Portugal": "PT", "Ireland": "IE", "Finland": "FI",
    "Greece": "GR", "Slovenia": "SI", "Croatia": "HR", "Slovakia": "SK", "Luxembourg": "LU",
    "Estonia": "EE", "Latvia": "LV", "Lithuania": "LT", "Cyprus": "CY", "Malta": "MT",
    "Andorra": "AD", "Monaco": "MC", "San Marino": "SM", "Montenegro": "ME",
    "United Kingdom": "GB", "Poland": "PL", "Czechia": "CZ", "Hungary": "HU",
    "Romania": "RO", "Bulgaria": "BG", "Sweden": "SE", "Denmark": "DK",
    "Norway": "NO", "Iceland": "IS", "Switzerland": "CH", "Albania": "AL",
    "Serbia": "RS", "Turkey": "TR", "Ukraine": "UA", "Russia": "RU", "Belarus": "BY",
    "Georgia": "GE", "Moldova": "MD", "Bosnia and Herzegovina": "BA",
    "Macedonia": "MK", "North Macedonia": "MK", "Czech Republic": "CZ", "Liechtenstein": "LI", "United States": "US",
    "Canada": "CA", "Mexico": "MX", "Brazil": "BR", "Argentina": "AR",
    "Chile": "CL", "Colombia": "CO", "Peru": "PE", "Uruguay": "UY",
    "Venezuela": "VE", "Ecuador": "EC", "El Salvador": "SV", "Costa Rica": "CR",
    "Guatemala": "GT", "Honduras": "HN", "Nicaragua": "NI", "Panama": "PA",
    "Paraguay": "PY", "Dominican Republic": "DO", "Jamaica": "JM",
    "Trinidad And Tobago": "TT", "Barbados": "BB", "Bahamas": "BS",
    "Belize": "BZ", "Guyana": "GY", "Suriname": "SR", "Haiti": "HT",
    "Puerto Rico": "PR", "Cuba": "CU", "Cayman Islands": "KY",
    "Curaçao": "CW", "Aruba": "AW", "Dominica": "DM", "Grenada": "GD",
    "Saint Lucia": "LC", "Bolivia": "BO", "Japan": "JP", "China": "CN",
    "South Korea": "KR", "India": "IN", "Indonesia": "ID", "Thailand": "TH",
    "Vietnam": "VN", "Philippines": "PH", "Malaysia": "MY", "Singapore": "SG",
    "Hong Kong": "HK", "Taiwan": "TW", "Pakistan": "PK", "Bangladesh": "BD",
    "Sri Lanka": "LK", "Nepal": "NP", "Myanmar": "MM", "Cambodia": "KH",
    "Laos": "LA", "Kazakhstan": "KZ", "Uzbekistan": "UZ", "Kyrgyzstan": "KG",
    "Armenia": "AM", "Azerbaijan": "AZ", "Turkmenistan": "TM", "Mongolia": "MN",
    "Afghanistan": "AF", "Iran": "IR", "Iraq": "IQ", "Israel": "IL",
    "Jordan": "JO", "Lebanon": "LB", "Syria": "SY", "Kuwait": "KW",
    "Saudi Arabia": "SA", "Qatar": "QA", "Bahrain": "BH", "Oman": "OM",
    "United Arab Emirates": "AE", "Yemen": "YE", "Maldives": "MV",
    "Bhutan": "BT", "Australia": "AU", "New Zealand": "NZ",
    "Nigeria": "NG", "South Africa": "ZA", "Egypt": "EG", "Morocco": "MA",
    "Algeria": "DZ", "Tunisia": "TN", "Kenya": "KE", "Ghana": "GH",
    "Tanzania": "TZ", "Ethiopia": "ET", "Sudan": "SD", "Zimbabwe": "ZW",
    "Zambia": "ZM", "Botswana": "BW", "Namibia": "NA", "Rwanda": "RW",
    "Uganda": "UG", "Mozambique": "MZ", "Angola": "AO", "Senegal": "SN",
    "Mali": "ML", "Burkina Faso": "BF", "Niger": "NE", "Cameroon": "CM",
    "Ivory Coast": "CI", "Madagascar": "MG", "Chad": "TD", "Libya": "LY",
}

def fetch_json(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())

def normalize_to_unified(data, rates, country):
    eur_price = data.get("eur")
    if eur_price is None:
        return None
    
    try:
        eur_val = float(eur_price)
    except (TypeError, ValueError):
        return None
    
    currency_code = COUNTRY_TO_CURRENCY.get(country, "EUR")
    rate = rates.get(currency_code, 1.0)
    local_val = round(eur_val * rate, 2)
    symbol = CURRENCY_SYMBOLS.get(country, currency_code)
    
    code = "EUR" if symbol == "€" else currency_code
    
    return {
        "eur": str(eur_val),
        "local": {
            "symbol": symbol,
            "code": code,
            "value": str(local_val)
        }
    }

def parse_tolls_data(data, rates):
    result = {}
    continent = data.get("continent")
    data_date = data.get("data_date")
    
    for country, prices in data.get("countries", {}).items():
        gasoline95 = normalize_to_unified(prices.get("gasoline95", {}), rates, country)
        diesel = normalize_to_unified(prices.get("diesel", {}), rates, country)
        lpg = normalize_to_unified(prices.get("lpg", {}), rates, country)
        
        result[country] = {
            "continent": continent,
            "data_date": data_date,
            "gasoline95": gasoline95,
            "diesel": diesel,
            "lpg": lpg,
        }
    return result

def parse_gasoline_prices(data, rates):
    result = {}
    for item in data.get("countries", []):
        country = item.get("country")
        usd_price = item.get("last")
        if usd_price is None:
            continue
        
        try:
            usd_val = float(usd_price)
        except (TypeError, ValueError):
            continue
        
        eur_val = round(usd_val / 1.17, 2)
        currency_code = COUNTRY_TO_CURRENCY.get(country, "EUR")
        rate = rates.get(currency_code, 1.0)
        local_val = round(eur_val * rate, 2)
        symbol = CURRENCY_SYMBOLS.get(country, currency_code)
        
        result[country] = {
            "continent": "world",
            "gasoline95": {
                "eur": str(eur_val),
                "local": {
                    "symbol": symbol,
                    "code": currency_code,
                    "value": str(local_val)
                }
            },
            "diesel": None,
            "lpg": None,
        }
        
        ref = item.get("reference")
        if ref:
            result[country]["_reference"] = ref
    return result

def parse_fuel_prices(data, rates):
    result = {}
    week = data.get("week")
    year = data.get("year")
    
    country_map = {
        "IE": "Ireland", "IS": "Iceland", "ES": "Spain", "IT": "Italy", "AT": "Austria",
        "AZ": "Azerbaijan", "AL": "Albania", "AD": "Andorra", "BE": "Belgium",
        "BG": "Bulgaria", "BA": "Bosnia and Herzegovina", "BY": "Belarus",
        "GB": "United Kingdom", "GR": "Greece", "GE": "Georgia", "DK": "Denmark",
        "EE": "Estonia", "CY": "Cyprus", "LV": "Latvia", "LT": "Lithuania",
        "LU": "Luxembourg", "LI": "Liechtenstein", "MT": "Malta", "MD": "Moldova",
        "MC": "Monaco", "NO": "Norway", "NL": "Netherlands", "DE": "Germany",
        "PL": "Poland", "PT": "Portugal", "MK": "North Macedonia", "RU": "Russia",
        "RO": "Romania", "SM": "San Marino", "RS": "Serbia", "SK": "Slovakia",
        "SI": "Slovenia", "TR": "Turkey", "HU": "Hungary", "UA": "Ukraine",
        "FR": "France", "FI": "Finland", "HR": "Croatia", "CZ": "Czechia",
        "ME": "Montenegro", "CH": "Switzerland", "SE": "Sweden",
    }
    
    for item in data.get("countries", []):
        country_code = item.get("country")
        country_name = country_map.get(country_code, country_code)
        fuels = item.get("fuels", {})
        
        currency_raw = item.get("currency", "€")
        currency_code = COUNTRY_TO_CURRENCY.get(country_name, "EUR")
        rate = rates.get(currency_code, 1.0)
        
        def to_eur(price):
            if price is None or price == 0:
                return None
            return round(price / rate, 2) if rate else price
        
        def to_local(price):
            if price is None:
                return None
            return round(price * rate, 2)
        
        a95 = fuels.get("A95", {}).get("currentPrice")
        diesel = fuels.get("Diesel", {}).get("currentPrice")
        lpg = fuels.get("LPG", {}).get("currentPrice")
        
        symbol = CURRENCY_SYMBOLS.get(country_name, currency_code)
        
        result[country_name] = {
            "continent": "europe",
            "week": week,
            "year": year,
            "gasoline95": {
                "eur": str(to_eur(a95)),
                "local": {"symbol": symbol, "code": currency_code, "value": str(to_local(a95))}
            } if a95 else None,
            "diesel": {
                "eur": str(to_eur(diesel)),
                "local": {"symbol": symbol, "code": currency_code, "value": str(to_local(diesel))}
            } if diesel else None,
            "lpg": {
                "eur": str(to_eur(lpg)),
                "local": {"symbol": symbol, "code": currency_code, "value": str(to_local(lpg))}
            } if lpg and lpg > 0 else None,
        }
    return result

def parse_reference_date(ref):
    if not ref:
        return None
    months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
             "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    try:
        parts = ref.replace("/", " ").split()
        month = months.get(parts[0][:3], 1)
        year_str = parts[1] if len(parts) > 1 else "26"
        year = int(year_str)
        year = 2000 + year if year < 100 else year
        return f"{year:04d}-{month:02d}-01"
    except:
        return None

def week_to_date(year, week):
    import datetime
    try:
        day = datetime.date(year, 1, 1) + datetime.timedelta(weeks=week - 1, days=-datetime.date(year, 1, 1).weekday())
        return day.isoformat()
    except:
        return None

def get_data_date(source_name, data):
    if source_name in ["america", "asia", "europe"]:
        return data.get("data_date"), None
    elif source_name == "gasoline":
        ref = data.get("_reference")
        if ref:
            return parse_reference_date(ref), ref
    elif source_name == "fuel":
        week = data.get("week")
        year = data.get("year")
        if week and year:
            return week_to_date(year, week), None
    return None, None

def get_freshest_data(source_name, existing, new):
    if not existing:
        return new
    
    existing_date = existing.get("_data_date") or ""
    new_date = new.get("_data_date") or ""
    
    if not existing_date:
        return new
    if not new_date:
        return existing
    
    return new if new_date > existing_date else existing

def merge_data(sources_data, existing_data=None):
    merged = {}
    
    for source_name, sources in sources_data.items():
        for source in sources:
            for country, data in source.items():
                d_date, ref = get_data_date(source_name, data)
                data["_data_date"] = d_date
                data["_reference"] = ref
                
                if country not in merged:
                    merged[country] = data
                else:
                    merged[country] = get_freshest_data(source_name, merged[country], data)
    
    for country, data in merged.items():
        data["country_code"] = COUNTRY_CODE.get(country)
        d = data.pop("_data_date", None)
        ref = data.pop("_reference", None)
        if d:
            data["data_date"] = d
        elif ref:
            data["data_date"] = ref
        data.pop("year", None)
        data.pop("week", None)
    
    if existing_data:
        existing = existing_data.get("data", {})
        for country, new_data in merged.items():
            new_date = new_data.get("data_date")
            old_entry = existing.get(country, {})
            old_date = old_entry.get("data_date")
            
            history = old_entry.get("history", []) or []
            
            if old_date and new_date and old_date != new_date:
                history_dates = {h.get("data_date") for h in history}
                if old_date not in history_dates:
                    g95 = old_entry.get("gasoline95")
                    diesel = old_entry.get("diesel")
                    lpg = old_entry.get("lpg")
                    history.insert(0, {
                        "data_date": old_date,
                        "gasoline95": g95.get("eur") if g95 else None,
                        "diesel": diesel.get("eur") if diesel else None,
                        "lpg": lpg.get("eur") if lpg else None,
                    })
            
            if history:
                new_data["history"] = history[:30]
    
    return merged

def main():
    import sys
    input_file = sys.argv[1] if len(sys.argv) > 1 else "merged_fuel_prices.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    rates_data = fetch_json(URLS["currency_rates"])
    rates = rates_data.get("rates", {})
    
    with open("currency_rates.json", "w", encoding="utf-8") as f:
        json.dump(rates_data, f, indent=2, ensure_ascii=False)
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            existing_data = json.loads(content) if content else None
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = None
    
    sources_data = {
        "america": [parse_tolls_data(fetch_json(URLS["america"]), rates)],
        "asia": [parse_tolls_data(fetch_json(URLS["asia"]), rates)],
        "europe": [parse_tolls_data(fetch_json(URLS["europe"]), rates)],
        "gasoline": [parse_gasoline_prices(fetch_json(URLS["gasoline"]), rates)],
        "fuel": [parse_fuel_prices(fetch_json(URLS["fuel"]), rates)],
    }
    
    merged = merge_data(sources_data, existing_data)
    
    output = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "sources": list(URLS.keys())[:-1],
        "data": merged
    }
    
    json_output = json.dumps(output, indent=2, ensure_ascii=False)
    
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_output)
    else:
        print(json_output)

if __name__ == "__main__":
    main()
