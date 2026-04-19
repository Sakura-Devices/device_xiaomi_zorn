#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/zorn',
    'hardware/qcom-caf/wlan',
    'hardware/qcom-caf/sm8650',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}-{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.diaghal@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
        'vendor.qti.ImsRtpService-V1-ndk'
    ): lib_fixup_vendor_suffix,
    (
        'android.hardware.graphics.composer3-V1-ndk',
        'android.hardware.graphics.allocator-V1-ndk',
        'android.hardware.graphics.composer3-V2-ndk',
        'audio.primary.pineapple',
        'libmilut',
        'libmips',
        'libmisr',
        'libagmclient',
        'libagmmixer',
        'libar-acdb',
        'libats',
        'liblx-osal',
        'liblx-ar_util',
        'libar-gpr',
        'libar-gsl',
        'libpalclient',
        'libwpa_client',
        'vendor.qti.hardware.display.composer3-V1-ndk',
        'vendor.qti.hardware.AGMIPC@1.0-impl',
        'vendor.qti.hardware.pal@1.0-impl',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'odm/etc/camera/enhance_motiontuning.xml',
        'odm/etc/camera/motiontuning.xml'
    ): blob_fixup()
        .regex_replace('xml=version', 'xml version'),
    (
        'odm/lib64/libMiPhotoFilter.so',
        'odm/lib64/libwa_widelens_undistort.so',
    ): blob_fixup()
    .clear_symbol_version('AHardwareBuffer_allocate')
    .clear_symbol_version('AHardwareBuffer_describe')
    .clear_symbol_version('AHardwareBuffer_isSupported')
    .clear_symbol_version('AHardwareBuffer_lock')
    .clear_symbol_version('AHardwareBuffer_lockPlanes')
    .clear_symbol_version('AHardwareBuffer_release')
    .clear_symbol_version('AHardwareBuffer_unlock'),
    (
        'odm/lib64/libcamxcommonutils.so',
        'vendor/lib64/libcameraopt.so',
        'odm/lib64/hw/camera.qcom.so'
    ): blob_fixup()
        .add_needed('libprocessgroup_shim.so'),
    (
        'odm/lib64/camera/plugins/com.xiaomi.plugin.jpegrAggr.so'
    ): blob_fixup()
        .add_needed('libcamerahdr_shim.so'),
    (
        'odm/lib64/com.qti.qseeaon.so'
    ): blob_fixup()
        .add_needed('libcameraflare_shim.so'),
    (
        'odm/lib64/camera/plugins/com.xiaomi.plugin.gainmap.so'
    ): blob_fixup()
        .add_needed('libcameraplugin_shim.so'),
    (
        'vendor/bin/hw/vendor.dolby.media.c2@1.0-service',
    ): blob_fixup()
        .add_needed('libshim.so'),
    'vendor/etc/sensors/hals.conf': blob_fixup()
        .add_line_if_missing('sensors.xiaomi.v2.so'),
    (
        'vendor/etc/media_codecs_pinaepple.xml', 
        'vendor/etc/media_codecs_pinaepple_vendor.xml'
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so')
        .add_needed('libbinder_shim.so'),
    (
        'vendor/lib64/libqcc_sdk.so', 
        'vendor/lib64/libqms_xiaomi.so',
        'vendor/lib64/libqms_client.so',
        'vendor/bin/qcc-vendor',
        'vendor/bin/xtra-daemon',
        'vendor/bin/qms',
        'vendor/bin/cnd',
        'vendor/lib64/libcne.so'
    ): blob_fixup()
        .add_needed('libbinder_shim.so'),
    ('odm/lib64/hw/camera.xiaomi.so'): blob_fixup()
        .replace_needed('libui.so', 'libui-v34.so'),
    (
        'vendor/lib64/libqcodec2_core.so',
    ):blob_fixup()
        .add_needed('libcodec2_shim.so'),
    (
        'vendor/lib64/libcapiv2uvvendor.so',
        'vendor/lib64/liblistensoundmodel2vendor.so',
        'vendor/lib64/libVoiceSdk.so',
    ): blob_fixup().replace_needed(
        'libtensorflowlite_c.so',
        'libtensorflowlite_c_vendor.so',
    ),
    ('odm/lib64/libaudioroute_ext.so',
     'vendor/lib64/libar-pal.so',
     'vendor/lib64/libagm.so'): blob_fixup()
        .replace_needed('libaudioroute.so', 'libaudioroute-v34.so'),
    'vendor/lib64/hw/audio.primary.pineapple.so': blob_fixup()
        .add_needed('libaudioroute-v34.so'),
    (
        'vendor/lib64/libdlbdsservice.so',
        'vendor/lib64/libdlbpreg.so',
        'vendor/lib64/soundfx/libdlbvol.so',
        'vendor/lib64/soundfx/libhwdap.so',
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    (
        'vendor/lib64/libaodoptfeature.so',
        'vendor/lib64/libapengine.so',
        'vendor/lib64/libdpps.so',
        'vendor/lib64/libgamepoweroptfeature.so',
        'vendor/lib64/liblearningmodule.so',
        'vendor/lib64/liboffscreenpoweroptfeature.so',
        'vendor/lib64/libpowercallback.so',
        'vendor/lib64/libpowercore.so',
        'vendor/lib64/libpsmoptfeature.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
        'vendor/lib64/libstandbyfeature.so',
        'vendor/lib64/libvideooptfeature.so',
        'odm/lib64/hw/displayfeature.default.so',
        'vendor/bin/hw/vendor.qti.hardware.display.composer-service',
        'vendor/bin/poweropt-service',
        'vendor/bin/qvrdatauploader',
        'odm/bin/hw/vendor.xiaomi.sensor.citsensorservice.aidl',
    ): blob_fixup()
        .replace_needed(
            'libtinyxml2.so',
            'libtinyxml2-v34.so',
    ),

        'odm/lib64/hw/displayfeature.default.so': blob_fixup()
            .replace_needed(
                'android.hardware.sensors-V2-ndk.so',
                'android.hardware.sensors-V3-ndk.so',
            )
            .replace_needed(
                'libtinyxml2.so',
                'libtinyxml2-v34.so',
    ),
}  # fmt: skip

module = ExtractUtilsModule(
    'zorn',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
    add_firmware_proprietary_file=True
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
