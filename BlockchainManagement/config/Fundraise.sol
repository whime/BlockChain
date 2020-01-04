pragma solidity ^0.5.0;

import "./Charity.sol";

contract Fundraise
{

    struct Multihash
    {
        bytes32 digest;
        uint8 hashFunction;
        uint8 size;
    }

    enum FundraiseState
    {
        Collecting,
        Disapproved,
        CharityClosed,
        OwnerClosed
    }

    /// @title 标识这个筹款项目的状态
    FundraiseState public state;
    /// @title 筹款项目的名字
    string public name;
    /// @title 所属慈善机构
    Charity public charity;
    /// @title 筹款项目的受益人
    address payable public owner;
    /// @title 筹款项目的发布人
    address payable public deployer;
    /// @title 目标金额
    uint public targetMoney;
    /// @title 当前金额
    uint public nowMoney;
    /// @title 表示筹款项目详细信息的IPFS地址
    Multihash[] public ipfsHashes;
    /// @title 临时保存捐赠人
    address payable[] internal donaters;
    /// @title 临时保存捐赠的金额
    mapping(address => uint) internal donationStorage;

    /// @notice 捐款已经达到上限
    event MoneyReached();
    /// @notice 筹款项目状态改变
    event FundraiseStateChanged();
    event Refunded(address donater, uint amount);

    constructor(string memory _name, Charity _charity, address payable _owner, uint _targetMoney) public
    {
        name = _name;
        charity = _charity;
        owner = _owner;
        deployer = msg.sender;
        targetMoney = _targetMoney;
        nowMoney = 0;
        state = FundraiseState.Collecting;
        _charity.addFundraise(this);
    }

    /// @notice 为筹款添加文件
    function addFile(bytes32 _digest, uint8 _hashFunction, uint8 _size) public payable
    {
        require(msg.sender == deployer, "Only deployer can add file");
        Multihash memory hash = Multihash(_digest, _hashFunction, _size);
        ipfsHashes.push(hash);
    }

    /// @notice 获取文件总数
    function getFileCount() public view returns(uint)
    {
        return ipfsHashes.length;
    }

    /// @notice 向受益人捐款，捐款临时存储在合约账户中
    function donate(uint value) public payable
    {
        require(state == FundraiseState.Collecting, "Only collecting fundraise can be donated");
        require(value > 0, "Amount must be larger than 0");
        require(msg.value >= value, "You must have enough money");
        //如果没捐过就插入捐赠人名单
        if(donationStorage[msg.sender] == 0)
            donaters.push(msg.sender);
        //临时存储捐钱，存入合约账户
        donationStorage[msg.sender] += msg.value;
        nowMoney += value;
        //到了上限，通知
        if(nowMoney >= targetMoney)
            emit MoneyReached();
    }

    /// @notice 慈善机构驳回筹款
    function disapproveFundraise() public payable
    {
        require(msg.sender == charity.charity(), "Only charity owner can disapprove fundraise");
        require(state == FundraiseState.Collecting, "Only collecting fundraise can be disapproved");
        state = FundraiseState.Disapproved;
        //退款
        for(uint i = 0; i < donaters.length; i++)
        {
            uint amount = donationStorage[donaters[i]];
            if(amount > 0)
            {
                //如果退款成功，则设置清空相应人员在合约的存款，否则保留，让捐款人可以自行退款
                donationStorage[donaters[i]] = 0;
                if(!donaters[i].send(amount))
                {
                    donationStorage[donaters[i]] = amount;
                }
                else
                {
                    emit Refunded(donaters[i], amount);
                }
            }
        }
    }

    /// @notice 慈善机构或受益人关闭筹款
    function closeFundraise() public payable
    {
        require(msg.sender == charity.charity() || msg.sender == owner, "Only charity or fundraiser owner can close fundraise");
        require(state == FundraiseState.Collecting, "Only collecting fundraise can be disapproved");
        //如果是慈善机构关闭
        if(msg.sender == charity.charity())
        {
            //将现有款项打给受益人
            owner.transfer(address(this).balance);
            //标记关闭
            state = FundraiseState.CharityClosed;
        }
        //如果是受益人关闭
        else
        {
            //标记关闭
            state = FundraiseState.OwnerClosed;
            //将所有款项退回给捐款人
            for(uint i = 0; i < donaters.length; i++)
            {
                uint amount = donationStorage[donaters[i]];
                if(amount > 0)
                {
                    //如果退款成功，则设置清空相应人员在合约的存款，否则保留，让捐款人可以自行退款
                    donationStorage[donaters[i]] = 0;
                    if(!donaters[i].send(amount))
                    {
                        donationStorage[donaters[i]] = amount;
                    }
                    else
                    {
                        emit Refunded(donaters[i], amount);
                    }
                }
            }
        }
    }

}