$(document).ready(function(){

	/* Underlie the navbar items on hover */
	$('.underline').parent().hover(
		function(){
			$(this).find('.underline').animate({ bottom: '5'}, 100);
		},
		function(){
			$(this).find('.underline').animate({ bottom: '-5'}, 100);
		}
	);

});