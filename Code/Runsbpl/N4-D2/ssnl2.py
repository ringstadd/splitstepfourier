import sys
import os
import numpy as np
import math
import param
import matplotlib.pyplot as plt
from matplotlib import animation
'''This program will do it's best to compute the split-step 
fourier transform to model nonlinear optical pulse propogation'''

if __name__ == '__main__':
    
    #Arrays

    tau =param.dtau*np.arange(-param.nt/2,param.nt/2)
    plt.clf
    omega = math.pi/param.Tmax*np.fft.ifftshift(np.linspace(-param.nt/2,param.nt/2, num=param.nt))


    #Input Field Profile

    if param.mshape == 0:
        uu=np.cosh(tau)**-1*np.exp(-0.5j*param.chirp0*tau**2) #soliton
    else:
        uu = np.exp(-0.5*(1+1j*param.chirp0)*tau**(2*param.mshape))

    #Plot Spectrum
    spec =np.fft.fftshift( np.fft.ifft(uu))*param.nt*param.dtau/np.sqrt(2.*np.pi)
    freq = np.fft.fftshift(np.fft.fftfreq(param.nt,d=param.dtau))
    f4 = plt.figure()
    plt.subplot(2,1,1)
    plt.plot(tau, np.absolute(uu)**2, 'ko-') 
    plt.xlim([-5,5])
    plt.title('Power of Input Pulse')
    plt.xlabel('Time')
    plt.subplot(2,1,2)
    plt.plot(np.fft.fftshift(omega)/(2*np.pi), np.absolute(spec)**2, 'ko-')
    plt.xlim([-.5,.5])
    plt.title('Power of Spectrum')
    plt.xlabel('Frequency')
    #Store Dispersion
    dispersion = np.exp(1j*0.5*param.beta2*omega**2*param.deltaz)
    hhz = 1j*param.N**2*param.deltaz

    #use symmetrized split step method
    A = np.zeros((param.stepNum,param.nt))
    Wt = np.zeros((param.stepNum,param.nt))
    temp =uu*np.exp(np.absolute(uu)**2*hhz/2)
    for x in range(int(param.stepNum)):
        fTemp= np.fft.ifft(temp)*dispersion
        uu = np.fft.fft(fTemp)
        temp= uu*np.exp(np.absolute(uu)**2*hhz)
        A[x,:]=np.fft.ifftshift(np.fft.ifft(uu))*(param.nt*param.dtau)/(np.sqrt(2*np.pi))
        Wt[x,:]=(temp)*np.exp(-np.absolute(uu)**2*hhz/2)
        print x
    uu = temp*np.exp(-np.absolute(uu)**2*hhz/2) #Final Field
    temp = np.fft.ifftshift(np.fft.ifft(uu))*(param.nt*param.dtau)/(np.sqrt(2*np.pi))
   # plt.close('all')
    f2 = plt.figure()
    plt.subplot(2,1,1)
    plt.plot(tau, np.absolute(uu)**2, 'ko-')
    plt.subplot(2,1,2)
    plt.plot(freq, np.absolute(temp*param.dtau)**2, 'ko-')

    z = np.linspace(0,param.distance,num=param.stepNum)
    print 'Test 1'

    f=plt.figure()
    plt.subplot(121)
    print 'Test 2'
    A[np.abs(A)==0]=10**-14
    Aout = 10*np.log10(np.abs(A)**2)
    print 'Test3'
    MLmax = np.max(Aout)
    plt.pcolormesh(freq, z, Aout,vmax=MLmax, vmin=MLmax-40)
    plt.autoscale(tight=True)
    print 'test 4'
    plt.xlim([-5,5])
    plt.xlabel('(f-f_0)')
    plt.ylabel('z')
   # 
    plt.subplot(122)
    Wt[np.abs(Wt)==0]=10**-14
    print 'test5'
    Wtout = 10*np.log10(np.abs(Wt)**2)
    WTmax = np.max(Wtout)
    plt.pcolormesh(tau, z, Wtout,vmax=WTmax, vmin=WTmax-40)
    plt.xlim([-10,10])
    print 'test6'
    #plt.autoscale(tight=True)
    plt.xlabel('(t-t0)')
    plt.ylabel('z')
    print 'test7'#
    plt.savefig('bigsol.png')
    plt.figure(f4.number)
    plt.subplot(2,1,2)
    plt.plot(np.fft.fftshift(omega/2/np.pi),np.abs(temp)**2)
    plt.xlim([-.5,.5])
    plt.ylim([0,2])
    plt.subplot(2,1,1)
    plt.plot(tau, np.abs(uu)**2)
    plt.xlim([-5,5])
    plt.savefig("bigsol-spec.eps")
    print 'test9'
    #f.savefig('nzero.eps')    

    #Create animation

#    fig = plt.figure()
#    ax = plt.axes(xlim=(-9,9), ylim=(0,10))
#    line,= ax.plot([],[],lw=2)

    def init():
        line.set_data([],[])
        return line,

    def animate(i):
        x = freq
        y = A[i,:]
        line.set_data(x,y)
        return line,

#    anim = animation.FuncAnimation(fig, animate, init_func=init, frames = np.int(param.stepNum), interval = 40,blit=True)

 #   anim.save('waveprop.mp4', fps=30)

    print 'test 8'
   # plt.figure(f)
    plt.show()
