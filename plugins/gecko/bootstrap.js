// See https://developer.mozilla.org/en-US/Add-ons/Bootstrapped_extensions

function startup(aData, aReason) {
  console.log("startup", arguments);
}

function shutdown(aData, aReason) {
  console.log("shutdown", arguments);
}

function install(aData, aReason) {
  console.log("install", arguments);
}

function uninstall(aData, aReason) {
  console.log("uninstall", arguments);

  if (aReason == ADDON_UNINSTALL) {
    console.log('really uninstalling');
  } else {
    console.log('not a permanent uninstall, likely an upgrade or downgrade');
  }
}
