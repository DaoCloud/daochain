pragma solidity ^0.4.2;

/*import {DaoHubAccount} from 'DaoHubAccount.sol';*/

contract DaoHubVerify {
    address daocloud;
    function DaoHubVerify(){
        daocloud = msg.sender;
    }

    struct Image {
        bytes32 imageHash;
        address owner;
        bytes repoTag;
        bytes32 imageId;
        // bool exist;
    }

    mapping(address => mapping(bytes => Image)) ownerIdImageMap;

    event regImage(bytes32 imageHash,
                   address owner,
                   bytes repoTag,
                   bytes32 imageId);


    function registerImage(bytes32 imageHash,
                           bytes repoTag,
                           bytes32 imageId){
        ownerIdImageMap[msg.sender][repoTag] = Image(imageHash, msg.sender, repoTag, imageId);
        regImage(imageHash, msg.sender, repoTag, imageId);
    }

    function queryImage(address owner, bytes repoTag)
        constant returns(bytes32, address, bytes, bytes32){
        Image memory i = ownerIdImageMap[owner][repoTag];
        return (i.imageHash, i.owner, i.repoTag, i.imageId);
    }
}
