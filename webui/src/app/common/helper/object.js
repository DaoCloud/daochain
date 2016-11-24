export function isEmpty(obj) {

  // null and undefined are 'empty'
  if (obj === null || obj === undefined) {
    return true;
  }

  // Assume if it has a length property with a non-zero value
  // that that property is correct.
  if (obj.length > 0) {
    return false;
  }

  if (obj.length === 0) {
    return true;
  }

  // Otherwise, does it have any properties of its own?
  // Note that this doesn't handle
  // toString and valueOf enumeration bugs in IE < 9
  for (var key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      return false;
    }
  }

  return true;
}

export function emptyObject(obj) {
  for (var x in obj) {
    delete obj[x];
  }
}
