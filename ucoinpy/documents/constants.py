
pubkey_regex = "(?![OIl])[1-9A-Za-z]{42,45}"
signature_regex = "[A-Za-z0-9+/]+(?:=|==)?"
block_hash_regex = "[0-9a-fA-F]{5,64}"
transaction_hash_regex = "[0-9a-fA-F]{5,64}"
block_id_regex = "[0-9]+"
block_uid_regex = "{block_id_regex}-{block_hash_regex}".format(block_id_regex=block_id_regex,
                                                              block_hash_regex=block_hash_regex)