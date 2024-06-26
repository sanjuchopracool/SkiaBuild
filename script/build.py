#! /usr/bin/env python3

import common, os, subprocess, sys

def main():
  os.chdir(os.path.join(os.path.dirname(__file__), os.pardir, 'skia'))

  build_type = common.build_type()
  machine = common.machine()
  system = common.system()
  ndk = common.ndk()

  # if build_type == 'Debug':
  #   args = ['is_debug=true']
  # else:
  args = ['is_official_build=true',
          'is_debug=false']

  args += [
    'target_cpu="' + machine + '"',
  ]

  if 'macos' == system:
    args += [
      'skia_use_system_expat=false',
      'skia_use_system_libjpeg_turbo=false',
      'skia_use_system_libpng=false',
      'skia_use_system_libwebp=false',
      'skia_use_system_zlib=false',
      'skia_use_sfntly=false',
      'skia_use_freetype=true',
      # 'skia_use_harfbuzz=true',
      'skia_use_system_harfbuzz=false',
      'skia_pdf_subset_harfbuzz=true',
      # 'skia_use_icu=true',
      'skia_use_system_icu=false',
      # 'skia_enable_skshaper=true',
      # 'skia_enable_svg=true',
      'skia_enable_skottie=true',
      'skia_use_system_freetype2=false',
      # 'skia_enable_gpu=true',
      'skia_use_metal=true',
      'extra_cflags_cc=["-frtti"]'
    ]
    if 'arm64' == machine:
      args += ['extra_cflags=["-stdlib=libc++"]']
    else:
      args += ['extra_cflags=["-stdlib=libc++", "-mmacosx-version-min=10.13"]']
  elif 'linux' == system:
    args += [
      'skia_use_system_expat=false',
      'skia_use_system_libjpeg_turbo=false',
      'skia_use_system_libpng=false',
      'skia_use_system_libwebp=false',
      'skia_use_system_zlib=false',
      'skia_use_sfntly=false',
      'skia_use_freetype=true',
      # 'skia_use_harfbuzz=true',
      'skia_use_system_harfbuzz=false',
      'skia_pdf_subset_harfbuzz=true',
      # 'skia_use_icu=true',
      'skia_use_system_icu=false',
      # 'skia_enable_skshaper=true',
      # 'skia_enable_svg=true',
      'skia_enable_skottie=true',
      'skia_use_system_freetype2=true',
      # 'skia_enable_gpu=true',
      'extra_cflags_cc=["-frtti"]',
    ]

    if (machine == 'arm64') and (machine != common.native_machine()):
      args += [
        'cc="aarch64-linux-gnu-gcc"',
        'cxx="aarch64-linux-gnu-g++"',
        'extra_cflags=["-I/usr/aarch64-linux-gnu/include"]'
      ]
    else:
      args += [
        'cc="gcc"',
        'cxx="g++"',
      ]

  elif 'windows' == system:
    args += [
        'skia_use_system_libjpeg_turbo=false',
        'skia_use_system_zlib=false',
        'skia_use_system_harfbuzz=false',
        'skia_use_system_libpng=false',
        'skia_use_system_libwebp=false',
        'skia_use_system_icu=false',
        'skia_use_system_expat=false',
        'skia_use_system_freetype2=false',
    ]

    if 'x64' == machine:
      args += [r'clang_win="C:\Program Files\LLVM"']
      
    if build_type == 'Debug':
      args += [r'extra_cflags=["/MDd"]']
    else:
      args += [r'extra_cflags=["/MD"]']
  elif 'android' == system:
    args += [
      'skia_use_system_freetype2=false',
      'ndk="' + ndk + '"'
    ]

  out = os.path.join('out', build_type + '-' + machine)
  gn = 'gn.exe' if 'windows' == system else 'gn'
  print(args)
  subprocess.check_call([os.path.join('bin', gn), 'gen', out, '--args=' + ' '.join(args)])
  ninja = 'ninja.bat' if 'windows' == system else 'ninja'
  subprocess.check_call([os.path.join('..', 'depot_tools', ninja), '-C', out, 'skia', 'modules'])

  return 0

if __name__ == '__main__':
  sys.exit(main())
