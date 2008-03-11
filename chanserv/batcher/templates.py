import md5, os, hmac, time
from rc4 import RC4

try:
  import hashlib
  sha256 = hashlib.sha256
  sha256m = hashlib.sha256
except ImportError:
  import sha256 as __sha256
  sha256 = __sha256.sha256
  sha256m = __sha256

def generate_url(config, obj):
  s = os.urandom(4)
  r = RC4(md5.md5("%s %s" % (s, config["urlkey"])).hexdigest())
  a = r.crypt(obj["user.password"])
  b = md5.md5(md5.md5("%s %s %s %s" % (config["urlsecret"], obj["user.username"], a, s)).hexdigest()).hexdigest()
  obj["url"] = "%s?m=%s&h=%s&u=%s&r=%s" % (config["url"], a.encode("hex"), b, obj["user.username"].encode("hex"), s.encode("hex"))

def generate_resetcode(config, obj):
  if not config.has_key("__codegensecret"):
    config["__codegenhmac"] = hmac.HMAC(key=sha256(sha256("%s:codegenerator" % config["q9secret"]).digest()).hexdigest(), digestmod=sha256m)

  h = config["__codegenhmac"].copy()
  h.update(sha256("%s:%d" % (obj["user.username"], obj["user.lockuntil"])).hexdigest())

  obj["resetcode"] = h.hexdigest()
  print obj
  obj["lockuntil"] = time.ctime(obj["user.lockuntil"])

MAILTEMPLATES = {
  "mutators": {
    1: generate_url,
    3: generate_resetcode,
    5: generate_resetcode,
  },
  "sendto": {
    5: "prevemail",
  },
  "languages": {
    "en": {
      1: {
        "subject": "%(config.bot)s account registration",
        "body": """
Thank you for registering.
To get your password please visit:
%(url)s

In case you forget your login/password use:
/msg %(config.bot)s REQUESTPASSWORD %(user.username)s %(user.email)s

Make sure you've read the %(config.bot)s FAQ at %(config.siteurl)s for a complete
reference on Q's commands and usage.

 ** PLEASE READ %(config.securityurl)s --
    it contains important information about keeping your account secure.
    Note that QuakeNet Operators will not intervene if you fail to read
    the above URL and your account is compromised as a result.

PLEASE REMEMBER THAT UNUSED ACCOUNTS ARE AUTOMATICALLY REMOVED
AFTER %(config.cleanup)d DAYS, AND ALL CHANLEVS ARE LOST!

NB: Save this email for future reference.
""",
      },
      2: { "subject": "%(config.bot)s password request", "body": """
Your username/password is:

Username: %(user.username)s
Password: %(user.password)s

To auth yourself to %(config.bot)s, type the following command

   /MSG %(config.bot)s@%(config.server)s AUTH %(user.username)s %(user.password)s
""", },
      3: { "subject": "%(config.bot)s password change", "body": """
Your password has recently changed. If this was not requested by you,
please use:
/MSG %(config.bot)s RESET #%(user.username)s %(resetcode)s

You have until %(lockuntil)s to perform this command.
""", },
      4: { "subject": "%(config.bot)s account reset", "body": """
Your %(config.bot)s account settings have been restored:
  E-mail address: %(user.email)s
  Password:       %(user.password)s

Make sure you read the %(config.bot)s security FAQ at %(config.securityurl)s.
""", },
      5: { "subject": "%(config.bot)s email change", "body": """
Your email address has been changed on %(config.bot)s from %(prevemail)s to %(user.email)s.

If you did not request this please use:
/MSG %(config.bot)s RESET #%(user.username)s %(resetcode)s

You have until %(lockuntil)s to perform this command.
""", },
    },
  },
}