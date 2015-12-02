/*
 * Detect if mobile browsing
 
 */
var isMobile = null;

if (navigator.userAgent.match(/Android/i) ||
 navigator.userAgent.match(/webOS/i) ||
 navigator.userAgent.match(/iPhone/i) ||
 navigator.userAgent.match(/iPad/i) ||
 navigator.userAgent.match(/iPod/i) ||
 navigator.userAgent.match(/BlackBerry/) || 
 navigator.userAgent.match(/Windows Phone/i) || 
 navigator.userAgent.match(/ZuneWP7/i)
 ) {
	// some code
	isMobile = true;
 } else {
	isMobile = false; 
 }