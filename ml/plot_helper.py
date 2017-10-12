import pandas as pd
import matplotlib.pyplot as plt

def plot_frame(df):
    for col in df.columns.values:
        plt.figure(figsize=(16,3))
        plt.title(col)
        plt.plot(df.index, df[col])
        plt.show()

def plot_gyro(df):
    gyros = [['gx0','gy0','gz0'],['gx1','gy1','gz1']]
    for num in gyros:
        plt.figure(figsize=(16,3))
        plt.title("gyro")
        for col in num:
            plt.plot(df.index, df[col])
        plt.show()
        
def plot_acc(df):
    gyros = [['ax0','ay0','az0'],['ax1','ay1','az1']]
    for num in gyros:
        plt.figure(figsize=(16,3))
        plt.title("acc")
        for col in num:
            plt.plot(df.index, df[col])
        plt.show()
        
def plot_filter(t, old, new):
    plt.figure(figsize=(16,3))
    plt.plot(t, old, 'b-', label='data')
    plt.plot(t, new, 'g-', linewidth=2, label='filtered data')
    plt.legend()
    plt.show()