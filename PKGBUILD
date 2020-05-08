# Maintainer: valadaa48 <valadaa48@gmx.com>

pkgname=retrolauncher
pkgver=1.0.1
pkgrel=1
pkgdesc="Low resource launcher"
arch=('any')
url=https://github.com/valadaa48/retrolauncher
license=('GPL2')
depends=(
    python-evdev
    python-uinput
)
source=(
    20-retrolauncher-uinput.rules
    retrolauncher.py
    retrolauncher.service
    RetroLauncher.sh
)
md5sums=('b240977225748b85468cea092d464091'
         'b0e125925ff347bad7343890fde3d6b8'
         '05a7fcf94dfd2563b1d74c5e0c943dca'
         'd224a6e329d5bf2139a3c960464cbb36')

package() {
    install -d ${pkgdir}/etc/udev/rules.d
    install -d ${pkgdir}/roms/sh
    install -d ${pkgdir}/usr/bin

	install -m 755 retrolauncher.py ${pkgdir}/usr/bin/retrolauncher
	install -m 755 RetroLauncher.sh ${pkgdir}/roms/sh
	install -m 644 20-retrolauncher-uinput.rules ${pkgdir}/etc/udev/rules.d
	install -D retrolauncher.service -t ${pkgdir}/etc/systemd/system
}
