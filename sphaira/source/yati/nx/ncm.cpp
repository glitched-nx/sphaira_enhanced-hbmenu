#include "yati/nx/ncm.hpp"
#include "defines.hpp"
#include <memory>
#include <bit>
#include <cstring>
#include <cstdlib>

namespace sphaira::ncm {
namespace {

} // namespace

auto GetMetaTypeStr(u8 meta_type) -> const char* {
    switch (meta_type) {
        case NcmContentMetaType_Unknown: return "Unknown";
        case NcmContentMetaType_SystemProgram: return "SystemProgram";
        case NcmContentMetaType_SystemData: return "SystemData";
        case NcmContentMetaType_SystemUpdate: return "SystemUpdate";
        case NcmContentMetaType_BootImagePackage: return "BootImagePackage";
        case NcmContentMetaType_BootImagePackageSafe: return "BootImagePackageSafe";
        case NcmContentMetaType_Application: return "Application";
        case NcmContentMetaType_Patch: return "Patch";
        case NcmContentMetaType_AddOnContent: return "AddOnContent";
        case NcmContentMetaType_Delta: return "Delta";
        case NcmContentMetaType_DataPatch: return "DataPatch";
    }

    return "Unknown";
}

// taken from nxdumptool
auto GetMetaTypeShortStr(u8 meta_type) -> const char* {
    switch (meta_type) {
        case NcmContentMetaType_Unknown: return "UNK";
        case NcmContentMetaType_SystemProgram: return "SYSPRG";
        case NcmContentMetaType_SystemData: return "SYSDAT";
        case NcmContentMetaType_SystemUpdate: return "SYSUPD";
        case NcmContentMetaType_BootImagePackage: return "BIP";
        case NcmContentMetaType_BootImagePackageSafe: return "BIPS";
        case NcmContentMetaType_Application: return "BASE";
        case NcmContentMetaType_Patch: return "UPD";
        case NcmContentMetaType_AddOnContent: return "DLC";
        case NcmContentMetaType_Delta: return "DELTA";
        case NcmContentMetaType_DataPatch: return "DLCUPD";
    }

    return "UNK";
}

auto GetStorageIdStr(u8 storage_id) -> const char* {
    switch (storage_id) {
        case NcmStorageId_None: return "None";
        case NcmStorageId_Host: return "Host";
        case NcmStorageId_GameCard: return "GameCard";
        case NcmStorageId_BuiltInSystem: return "BuiltInSystem";
        case NcmStorageId_BuiltInUser: return "BuiltInUser";
        case NcmStorageId_SdCard: return "SdCard";
        case NcmStorageId_Any: return "Any";
    }

    return "Unknown";
}

auto GetAppId(u8 meta_type, u64 id) -> u64 {
    if (meta_type == NcmContentMetaType_Patch) {
        return id ^ 0x800;
    } else if (meta_type == NcmContentMetaType_AddOnContent) {
        return (id ^ 0x1000) & ~0xFFF;
    } else {
        return id;
    }
}

auto GetAppId(const NcmContentMetaKey& key) -> u64 {
    return GetAppId(key.type, key.id);
}

auto GetAppId(const PackagedContentMeta& meta) -> u64 {
    return GetAppId(meta.meta_type, meta.title_id);
}

auto GetContentIdFromStr(const char* str) -> NcmContentId {
    char lowerU64[0x11]{};
    char upperU64[0x11]{};
    std::memcpy(lowerU64, str, 0x10);
    std::memcpy(upperU64, str + 0x10, 0x10);

    NcmContentId nca_id{};
    *(u64*)nca_id.c = std::byteswap(std::strtoul(lowerU64, nullptr, 0x10));
    *(u64*)(nca_id.c + 8) = std::byteswap(std::strtoul(upperU64, nullptr, 0x10));
    return nca_id;
}

Result Delete(NcmContentStorage* cs, const NcmContentId *content_id) {
    bool has;
    R_TRY(ncmContentStorageHas(cs, std::addressof(has), content_id));
    if (has) {
        R_TRY(ncmContentStorageDelete(cs, content_id));
    }
    R_SUCCEED();
}

Result Register(NcmContentStorage* cs, const NcmContentId *content_id, const NcmPlaceHolderId *placeholder_id) {
    R_TRY(Delete(cs, content_id));
    return ncmContentStorageRegister(cs, content_id, placeholder_id);
}

} // namespace sphaira::ncm
