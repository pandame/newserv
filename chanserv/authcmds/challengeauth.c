/* Automatically generated by refactor.pl.
 *
 *
 * CMDNAME: challengeauth
 * CMDLEVEL: QCMD_SECURE | QCMD_NOTAUTHED
 * CMDARGS: 3
 * CMDDESC: Authenticates you on the bot using challenge response.
 * CMDFUNC: csa_dochallengeauth
 * CMDPROTO: int csa_dochallengeauth(void *source, int cargc, char **cargv);
 * CMDHELP: Usage: challengeauth <username> <response> <hmac algorithm>
 * CMDHELP: Authenticates using challenge response.
 * CMDHELP: To generate the response from the challenge, calculate the following:
 * CMDHELP:   HMAC(challenge){k}
 * CMDHELP: where HMAC is the hash message authentication code as described in
 * CMDHELP: RFC 2104, k is HEXDIGEST(<lower case username>:HEXDIGEST(<password>))
 * CMDHELP: and HEXDIGEST is the hash function used in the MAC construction.
 * CMDHELP: For example code see the website.
 */

#include "../chanserv.h"
#include <time.h>

int csa_auth(void *source, int cargc, char **cargv, CRAlgorithm alg);

int csa_dochallengeauth(void *source, int cargc, char **cargv) {
  CRAlgorithm alg;
  activeuser* aup;
  time_t t;
  nick *sender=(nick *)source;

  if(cargc<3) {
    chanservstdmessage(sender, QM_NOTENOUGHPARAMS, "challengeauth");
    return CMD_ERROR;
  }

  if (!(aup=getactiveuserfromnick(sender)))
    return CMD_ERROR;

  t = time(NULL);
  if(t > aup->entropyttl) {
    chanservstdmessage(sender, QM_NOCHALLENGE);
    return CMD_ERROR;
  }

  aup->entropyttl = 0;

  alg = cs_cralgorithm(cargv[2]);
  if(!alg) {
    chanservstdmessage(sender, QM_CHALLENGEBADALGORITHM);
    return CMD_ERROR;
  }

  return csa_auth(sender, cargc, cargv, alg);
}
