import re
import pandas as pd


def add_sort_data(data):
    with open(data, "r", encoding="utf-8") as file:
        all_content = file.read().split("*$*")[1:]
    all_cgn = []
    all_data = {}
    for index, applic in enumerate(all_content):
        text = applic
        text = re.sub(r'-\nN1', '-N1', text)
        print(index + 1, end=" ")
        try:
            pattern = re.compile(r'\b20\d+(?:-N1|\d|$)')
            matches = re.findall(pattern, text)
            match = ""
            for m in matches:
                if len(m) > 8:
                    match = m
                    break
            all_cgn.append(match)
            print(match)
            if match not in all_data:
                all_data[match] = text + "*%*"
            else:
                all_data[match] += text + "*%*"
        except ValueError:
            print(index + 1, text)
    sorted_dict = dict(sorted(all_data.items()))
    with open(f"sort_{data.replace('.dat', '')}.txt", 'w', encoding="utf-8") as file:
        for key, value in sorted_dict.items():
            file.write(f'{key}*$* {value}\n')
    return sorted_dict


if __name__ == "__main__":
    applic = add_sort_data("all_applic.dat")
    meta = add_sort_data("all_meta.dat")
    z = 0
    am = []
    all_CGN = list(set(list(applic.keys()) + list(meta.keys())))
    for i, CGN in enumerate(all_CGN):
        am.append([CGN, '', ''])
        if CGN in applic.keys():
            am[i][1] += (applic[CGN])
        if CGN in meta.keys():
            am[i][2] += (meta[CGN])
    my_dict = am
    df = pd.DataFrame(my_dict, columns=['applic', "meta", "important"])
    df.to_excel('output.xlsx', index=False)
