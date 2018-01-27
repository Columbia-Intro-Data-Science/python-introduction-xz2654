
public class CreditCard {
	private Money balance;
	private Money creditLimit;
	private Person owner;
	
	public CreditCard(Person newCardHolder, Money limit)
	{
		creditLimit=limit;
		owner=newCardHolder;
		balance=new Money(0);
	}
	public Money getBalance()
	{
		Money getbalance=new Money(balance);
		return getbalance;
	}
	public Money getCreditLimit()
	{
		Money getcreditLimit=new Money(creditLimit);
		return getcreditLimit;
	}
	public String getPersonals()
	{
		return owner.toString();
	}
	public void charge(Money amount)
	{	
		if(this.creditLimit.compareTo(this.balance.add(amount))==1)
		System.out.println("Charge: "+amount.toString());	
		this.balance=this.balance.add(amount);
		}
		 
		else 
			System.out.println("Exceeds credit limit");
	}
	public void payment(Money amount)
	{
		
		System.out.println("Payment: "+amount.toString());
		this.balance = new Money(this.balance.subtract(amount));
	}
}
