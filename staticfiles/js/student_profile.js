console.log("Hello from student_profile.js");

document.addEventListener("DOMContentLoaded", function() {

	const dialog = document.querySelector("#payment-record");
	const openDialogButton = document.querySelector("#payment-record-dailog");
	const closeDialogButton = document.querySelector("#close-dialog");

	openDialogButton.addEventListener("click", function(e) {
		e.preventDefault();
		dialog.showModal();
	});

	closeDialogButton.addEventListener("click", function(e) {
		e.preventDefault();
		dialog.close();
	});
})
