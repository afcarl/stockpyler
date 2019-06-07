import os
import sys
import subprocess
import shlex

def is_file(env,path):
    return os.path.isfile(os.path.abspath(env.subst(path)))
 
if sys.platform.startswith('win'):
    env = DefaultEnvironment(ENV=os.environ)
    env.Append(CPPDEFINES='_CRT_SECURE_NO_WARNINGS')
    env.Replace(CC='clang-cl')
    env.Replace(LINK='lld-link')
    env.Append(CFLAGS=' -Xclang -std=gnu11 -Xclang -fwrapv ')
    env.Append(LINKFLAGS=' -debug  /subsystem:console ')
else:
    if ARGUMENTS.get('use_gcc'):
        env = DefaultEnvironment(ENV=os.environ,tools=['mingw','gcc'])
        env.Replace(CC='gcc')
    else:
        env = DefaultEnvironment(ENV=os.environ)
        env.Replace(CC='clang')
        env.Append(LINKFLAGS= ' -fuse-ld=lld ')
        env.Append(CCFLAGS=' -Wno-gnu-statement-expression -Wno-language-extension-token ')
    env.Append(CFLAGS='-std=gnu11 -fwrapv -march=native -m64 ')
    
   
root_dir = Dir('.')
env.Replace(BUILD_ROOT=root_dir.get_abspath())
env.AddMethod(is_file,'IsFile')
env.Append(CPPPATH=['$BUILD_ROOT/inc',
                    '$BUILD_ROOT/src',
                    '$BUILD_ROOT/third-party',
                    '$BUILD_ROOT/third-party/sdl2/include',
                    '$BUILD_ROOT/third-party/sdl2_image/include',
                    '$BUILD_ROOT/third-party/sdl2_mixer/include',
                    '$BUILD_ROOT/third-party/sdl2_ttf/include',
                    '$BUILD_ROOT/third-party/glew/include',])


def print_cmd_line(s, target, source, env):
    if ARGUMENTS.get('verbose'):
        print(s)
    else:
        print("building " + str(source[0]))

#env['PRINT_CMD_LINE_FUNC'] = print_cmd_line

debug_env = env.Clone()
release_env = env.Clone()

if sys.platform.startswith('win'):
    debug_env.Append(CCFLAGS=' /Z7 ')
    release_env.Append(CCFLAGS=' -Xclang -O3 /Z7 ')
else:
    debug_env.Append(CCFLAGS=' -g ')
    release_env.Append(CCFLAGS=' -O3 ')
    if ARGUMENTS.get("ASAN"):
        debug_env.Append(CCFLAGS=' -fsanitize=address ')
        debug_env.Append(LINKFLAGS=' -fsanitize=address ')
    elif ARGUMENTS.get("UBSAN"):
        debug_env.Append(CCFLAGS=' -fsanitize=undefined ')
        debug_env.Append(LINKFLAGS=' -fsanitize=undefined ')

#prepend these so that all Wno all go after, regardless of where we actually do the append
debug_env.Prepend(CCFLAGS=' -Wall -Wextra  ')
if debug_env['CC'] != 'gcc':
    debug_env.Prepend(CCFLAGS=' -Weverything ')
    debug_env.Append(CCFLAGS=' -Wno-newline-eof -Wno-gnu-zero-variadic-macro-arguments -Wno-gnu-case-range -Wno-gnu-folding-constant -Wno-language-extension-token -Wno-gnu-statement-expression ')
else:
    debug_env.Append(CCFLAGS=' -Wsuggest-attribute=pure -Wsuggest-attribute=const ')

debug_env.Append(CCFLAGS=' -Og -Wno-missing-prototypes -Wno-unused-parameter  -Wno-unused-function -Wno-unused-macros -Wno-padded  -DDEBUG_BUILD ')

release_env.Append(CCFLAGS='  -DRELEASE_BUILD -Wno-unused-value')
release_env.Append(LINKFLAGS='  ')


ret = debug_env.SConscript('./SConscript.py',variant_dir='BIN_debug',exports={'env':debug_env},duplicate=False)
env.Alias('debug',ret)

ret = release_env.SConscript('./SConscript.py',variant_dir='BIN_release',exports={'env':release_env},duplicate=False)
env.Alias('release',ret)


def clang_format_func(env,target,source):
    for root, dirs, files in os.walk("./src", topdown=False):

        for name in files:
            if name.endswith('.c') or name.endswith('.h'):
                args = ['clang-format', '-i',  os.path.abspath(os.path.join(root,name))]
                subprocess.check_call(args)

    with open(str(target[0]), 'w+') as f:
        f.write(' ')

clang_format_builder = env.Builder(action=clang_format_func)
env.Append(BUILDERS={'ClangFormat':clang_format_builder})
ret = env.ClangFormat(target='dummyout.txt')
env.AlwaysBuild(ret)
env.Alias('clang_format',ret)



#gtest_env = env.Clone()
#gtest_env.Append(LINKFLAGS=' -pthread -lgtest ')
#gtest_env.Append(CPPPATH=['#third-party/googletest/include','#third-party/googletest'])
#gtest_env['DOING_GOOGLE_TEST']=True
#gtest_env.Append(CCFLAGS=' -DDOING_GOOGLE_TEST ')
#ret = gtest_env.SConscript('./SConscript.py',variant_dir='BIN_gtest',exports={'env':gtest_env},duplicate=False)
#env.Alias('gtest',ret,ret[0].abspath)