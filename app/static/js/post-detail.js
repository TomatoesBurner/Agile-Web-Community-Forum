let isCommentAccepted = false;  // 标志，用于跟踪是否已经有评论被采纳

function acceptComment(commentElement) {
  const currentUserId = '123'; // Assume this is the logged-in user's ID
  const authorId = commentElement.getAttribute('data-author-id');

  if (!isCommentAccepted && currentUserId === authorId) {
    commentElement.classList.add('accepted-comment');
    disableOtherComments();
    alert("Accepted successfully!");
    isCommentAccepted = true;  // 更新标志状态
  } else if (isCommentAccepted) {
    alert("You can only accept one comment.");
  } else {
    alert("You are not authorized to accept this comment.");
  }
}

function disableOtherComments() {
  const comments = document.querySelectorAll('.comment');
  comments.forEach((comment) => {
    if (!comment.classList.contains('accepted-comment')) {
      comment.classList.add('disabled-hover');
    }
  });
}