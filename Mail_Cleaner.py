import EFZP as zp
p = zp.parse("Hi Dave,\nLets meet up this Tuesday\nCheers, Tom\n\nOn Sunday, 15 May 2011 at 5:02 PM, Dave Trindall wrote: Hey Tom,\nHow about we get together ...")
print (str(p['body']), " ", str(p['reply_text']))

