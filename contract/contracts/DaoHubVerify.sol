pragma solidity ^0.4.2;

contract DaoHubVerify {
  struct Image {
    address author;
    bytes32 repoTag;
    bytes32 imageId;
  }

  mapping(bytes32 => Image) imageMap;

  event newImage(bytes32 imageHash,
                 address author,
                 bytes32 repoTag,
                 bytes32 imageId);

  function registerImage(bytes32 imageHash,
                         address author,
                         bytes32 repoTag,
                         bytes32 imageId){
    imageMap[imageHash] = Image(author, repoTag, imageId);
    newImage(imageHash, author, repoTag, imageId);
  }

  function getImageFromHash(bytes32 imageHash)
    constant returns(address author, bytes32 repoTag, bytes32 imageId){
      Image i = imageMap[imageHash];
      return (i.author, i.repoTag, i.imageId);
  }
}
