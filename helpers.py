import os
import numpy as np

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"

from ftplib import FTP
url = "ftp.geonet.org.nz"


def download_motion(station):
    ftp = FTP(url)
    ftp.login()
    year = "2010"
    day = "Sept04"
    eq = year + day

    folder_path = ROOT_DIR + "%s/" % eq

    ftp.cwd('strong/processed/2010/09_Darfield_mainshock_extended_pass_band/Vol2/data in csv format')
    print(ftp.dir)

    filenames = ftp.nlst()  # get filenames within the directory

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    for filename in filenames:
        if station in filename:
            print(filename)

            local_filename = folder_path + filename
            file = open(local_filename, 'wb')
            ftp.retrbinary('RETR ' + filename, file.write)

            file.close()

    ftp.quit()


def load_nz_motions_3comp_v2(ffp):
    data = np.loadtxt(ffp, skiprows=5, delimiter=",")
    dt = data[1][0] - data[0][0]
    acc1 = data[:, 1] / 1e3  # convert from mm/s2 to m/s2
    acc2 = data[:, 2] / 1e3
    accv = data[:, 3] / 1e3
    # Trim the two records to be the same length
    min_len = min(len(acc1), len(acc2), len(accv))
    if min_len % 2:
        min_len -= 1
    acc1 = acc1[:min_len]
    acc2 = acc2[:min_len]
    accv = accv[:min_len]
    return acc1, acc2, accv, dt


if __name__ == '__main__':
    download_motion('SHLC')