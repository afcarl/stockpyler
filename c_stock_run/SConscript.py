Import('env')

sources = env.Glob('src/*.c')

ret = []

lib_paths = []

libs = []
installs = []

for p in lib_paths:
    libs.extend(env.Glob(p + '*.lib'))
    installs.append(env.Install('.',env.Glob(p + '*.dll')))

ret.append(installs)
ret.append(env.Program('c4',[libs,sources,]))
Return('ret')
