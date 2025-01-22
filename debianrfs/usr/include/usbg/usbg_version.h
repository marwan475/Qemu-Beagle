/*
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 */

#ifndef USBG_VERSION_H
#define USBG_VERSION_H

/**
 * Make API version integer from major, minor and micro numbers
 */
#define USBG_MAKE_VERSION(major, minor, micro) \
	((major << 24) | (minor << 16) | micro)

/**
 * Version of libusbgx's that is available.
 */
#define USBG_VERSION	0x00020000

#endif
