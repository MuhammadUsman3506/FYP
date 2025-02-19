#!/usr/bin/python3
import argparse
import os
import json
import colorama
from colorama import Fore
f_name = "Baseboard.sv"
folder_name = 'Baseboard'
######################### setting name of instance & body  ############################


def set_instance_name(f_name, inputs, outputs, input_ranges, output_ranges):
    m_name = f_name.replace(".sv", "")
    if inputs or outputs:
        Body = f"module {m_name} (\ninput\tlogic\t\tclk,\ninput\tlogic\t\treset,"
        if inputs:
            i = ""
            for inp, inp_ranges in zip(inputs, input_ranges):
                if inp_ranges == 'None' or inp_ranges == 'none':
                    inpu = f"\ninput\tlogic\t\t{(i.join(inp))},"
                    Body = Body + inpu
                else:
                    inpu = f"\ninput\tlogic\t{inp_ranges}\t{(i.join(inp))},"
                    Body = Body + inpu
        if outputs:
            o = ""
            for out, opt_ranges in zip(outputs, output_ranges):
                if opt_ranges == 'None' or opt_ranges == 'none':
                    outu = f"\noutput\tlogic\t\t{o.join(out)},"
                    Body = Body + outu
                else:
                    outu = f"\noutput\tlogic\t{opt_ranges}\t{o.join(out)},"
                    Body = Body + outu
        Body = Body.rstrip(",")
        end = "\n\n);\nendmodule"
        Body = Body + end
        print(Body)
    else:
        Body = f'''module {m_name} (\ninput\tlogic\t\tclk,\ninput\tlogic\t\treset,\n\n);\nendmodule'''
        print(Body)
    return Body


#########################################################


def default():
    global inputs, outputs, f_name, input_ranges, output_ranges
    print(f_name)
    print(os.getcwd())
    try:
        os.makedirs(folder_name)
        os.chdir(folder_name)
        with open(f_name, 'w+') as file:
            file.write(set_instance_name(f_name, inputs,
                       outputs, input_ranges, output_ranges))
            print(Fore.LIGHTBLUE_EX + f"{f_name} created" + Fore.RESET)
    except:
        os.chdir(folder_name)
        with open(f_name, 'w+') as file:
            file.write(set_instance_name(f_name, inputs,
                       outputs, input_ranges, output_ranges))

            print(Fore.LIGHTBLUE_EX + f"{f_name} created" + Fore.RESET)
#########################################################


def name():
    global inputs, outputs, input_ranges, output_ranges
    print(os.getcwd())
    try:
        os.chdir(folder_name)
        with open(f_name, 'w+') as file:
            file.write(set_instance_name(f_name, inputs,
                       outputs, input_ranges, output_ranges))
            print(Fore.LIGHTBLUE_EX + f"{f_name} created" + Fore.RESET)
    except:
        os.makedirs(folder_name)
        os.chdir(folder_name)
        with open(f_name, 'w+') as file:
            file.write(set_instance_name(f_name, inputs,
                       outputs, input_ranges, output_ranges))
            print(Fore.LIGHTBLUE_EX + f"{f_name} created" + Fore.RESET)


#########################################################
def storing_data_in_Json(f_name, inputs, input_ranges, outputs, output_ranges):
    m_name = f_name.replace(".sv", "")

    ports = {}
    ports["clk"] = {"type": "input", "range": "None"}
    ports["reset"] = {"type": "input", "range": "None"}

    if inputs:
        for i, inp in enumerate(inputs):
            if type(inp) == list:
                inp = inp[0]
            ports[inp] = {"type": "input", "range": input_ranges[i]}
    if outputs:
        for j, out in enumerate(outputs):
            if type(out) == list:
                out = out[0]
            ports[out] = {"type": "output", "range": output_ranges[j]}

    module_dict = {m_name: {"ports": ports}}
    return m_name, module_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename',
                        default="Baseboard.sv", help='Name of the  top level file')
    parser.add_argument('-i', '--inputs', type=str,
                        nargs='+', help='Input port name')
    parser.add_argument('-ir', '--input_ranges', type=str,
                        nargs='+', help='Input port range')
    parser.add_argument('-o', '--outputs', type=str,
                        nargs='+', help='Output port name')
    parser.add_argument('-or', '--output_ranges',
                        nargs='+', help='Output port range')
    args = parser.parse_args()

    f_name = args.filename
    inputs = args.inputs
    input_ranges = args.input_ranges
    outputs = args.outputs
    output_ranges = args.output_ranges

    if f_name:
        name()
    else:
        default()
    m_name, module_dict = storing_data_in_Json(
        f_name, inputs, input_ranges, outputs, output_ranges)

    os.chdir('..')
    os.chdir('Baseboard')

    json_data = {
        "file_name": f"{f_name}",
        "folder_name": f"{folder_name}"
    }
    with open("key_val_file.json", "w") as jsonfile:
        body = '{\n\"toplevelfile\":'
        end_body = '\n}'
        jsonfile.write(body)
        json.dump(json_data, jsonfile, indent=4)
        jsonfile.write(end_body)

    with open("key_val_file.json", "rb") as f:
        content = f.read()
        f.seek(0, 2)
    with open('key_val_file.json', 'a+') as f:
        r_end = (f.tell())-1
        x = f.truncate(r_end)
        f.write(f',\"{m_name}\":')
        json.dump(module_dict[m_name], f, indent=4)
        f.write("\n}")


