function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};

if (port==7){
  
  var b_t = [bytes[0], bytes[1], bytes[2], bytes[3]];

  decoded.t1=b2f(b_t, 1, 8, 23, -126, 127, true);
}
  return decoded;
}



function b2f(bytes, signBits, exponentBits, fractionBits, eMin, eMax, littleEndian) {
           var totalBits = (signBits + exponentBits + fractionBits);
           var binary = "";
           for (var i = 0, l = bytes.length; i < l; i++) {
               var bits = bytes[i].toString(2);
               while (bits.length < 8)
                   bits = "0" + bits;
               if (littleEndian)
                   binary = bits + binary;
               else
                   binary += bits;
           }
           var sign = (binary.charAt(0) == '1') ? -1 : 1;
           var exponent = parseInt(binary.substr(signBits, exponentBits), 2) - eMax;
           var significandBase = binary.substr(signBits + exponentBits, fractionBits);
           var significandBin = '1' + significandBase;
           i = 0;
           var val = 1;
           var significand = 0;
           if (exponent == -eMax) {
               if (significandBase.indexOf('1') == -1)
                   return 0;
               else {
                   exponent = eMin;
                   significandBin = '0' + significandBase;
               }
           }
           while (i < significandBin.length) {
               significand += val * parseInt(significandBin.charAt(i));
               val = val / 2;
               i++;
           }
           return sign * significand * Math.pow(2, exponent);
       }
   
